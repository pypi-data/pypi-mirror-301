from updater.utils.amzn_handler import is_amazon_url
from updater.utils.amzn_handler import extract_asin_from_url, get_items_data_from_asins, search_pd_amzn
from updater.utils.ai_handler import get_openai_response
from updater.utils.google_handler import fetch_google_results
from updater.utils.db_handler import db_get_pd_id_by_asin, db_add_pd, db_add_brand_if_new, db_get_product_brand_by_pd_and_category, db_get_brand_by_pd_id, db_add_product_brand
from typing import Optional
from paapi5_python_sdk.models.item import Item
from pathlib import Path
import inflect
import asyncio

# Initialize lock to prevent race conditions when checking and adding products, brands, and product_brands to db
process_opn_w_db_lock = asyncio.Lock()

# Takes checked opns list and to each opn adds keys 'product_id'(int/None) and 'brand_id'(int/None)
async def furnish_pd_info(checked_opns: list[dict], pd_category_name: str) -> list[dict]:
  opns_w_asin = []
  opns_wo_asin = []
  
  # Add index to each opn for identification + initializes product_id and brand_id
  for opn in checked_opns:
    opn['index'] = checked_opns.index(opn)
    opn['product_id'] = None
    opn['brand_id'] = None
    opn['product_brand_id'] = None
    opn['asin'] = None
  
  # Check filtered opns for amzn urls (full or shortened) and split into groups
  for opn in checked_opns:
    print(f'\nChecking for amzn urls for: {opn["username"]}...')
    initial_url = opn['pd_url']
    if initial_url and is_amazon_url(initial_url):
      opn['asin'] = extract_asin_from_url(initial_url) # Extracts asin from URL even if shortened
      if opn['asin']:
        opns_w_asin.append(opn)
        print(f'-> ASIN found, no need to search: {initial_url}')
      else:
        opns_wo_asin.append(opn)
        print(f'-> ASIN NOT found: {initial_url}')
    else:
      print(f'-> Amzn url NOT found for: {opn["username"]}')
      opns_wo_asin.append(opn)

  # Process both groups sequentially
  print(f'\nProcessing {len(opns_w_asin)} opns with asin...')
  processed_opns = []
  for opn in opns_w_asin:
    processed_opn = await process_opn_w_asin(opn, opn['asin'])
    processed_opns.append(processed_opn)

  print(f'\nProcessing {len(opns_wo_asin)} opns without asin...')
  for opn in opns_wo_asin:
    processed_opn = await process_opn_wo_asin(opn, pd_category_name)
    processed_opns.append(processed_opn)

  # Filter out opns that don't at least have a brand_id
  opns_w_brand_id = [opn for opn in processed_opns if opn['brand_id']]
  
  # Replace opns in checked_opns for those in opns_w_brand_id
  for opn in checked_opns:
    for opn_w_brand_id in opns_w_brand_id:
      if opn['index'] == opn_w_brand_id['index']:
        opn['brand_id'] = opn_w_brand_id['brand_id']
        opn['product_id'] = opn_w_brand_id['product_id']
        break

  return checked_opns



async def process_opn_w_asin(opn: dict, asin: str) -> dict:
  pd_category_id = opn['pd_category_id']
  
  # Lock to prevent race conditions when checking and adding brands and products
  async with process_opn_w_db_lock:
    # Check supabase if asin is already in products table
    db_pd_id = await db_get_pd_id_by_asin(asin)
    
    # If db has product with asin...
    if db_pd_id:
      # Set product_id
      opn['product_id'] = db_pd_id
      
      # If product_brand exists (incl correct category), set brand_id & product_brand_id
      product_brand = await db_get_product_brand_by_pd_and_category(db_pd_id, pd_category_id)
      if product_brand:
        opn['product_brand_id'] = product_brand['id']
        opn['brand_id'] = product_brand['brands']['id']
      # If product_brand does not exist, add brand using brand name and pd_category_id, then add product_brand to db
      else:
        brand_template = await db_get_brand_by_pd_id(db_pd_id)
        brand_name = brand_template['name_full']
        new_brand = await db_add_brand_if_new(brand_name, pd_category_id)
        opn['brand_id'] = new_brand['id']
        opn['product_brand_id'] = (await db_add_product_brand(db_pd_id, new_brand['id']))['id']
    
    # If asin doesn't exist, call amzn api, add to db, then set product_id and brand_id
    else:
      amzn_items = await get_items_data_from_asins([asin])
      if amzn_items:
        amzn_item = amzn_items[0]
        product_id, brand_id, product_brand_id = await add_amzn_item_to_db(amzn_item, pd_category_id)
        opn['product_id'] = product_id
        opn['brand_id'] = brand_id
        opn['product_brand_id'] = product_brand_id
  
  return opn


async def process_opn_wo_asin(opn: dict, pd_category_name: str) -> dict:
  # If no brand identified but url exists, try to get brand from url (None if cannot find)
  if not opn['pd_brand'] and opn['pd_url']:
    opn['pd_brand'] = await get_pd_brand(opn['pd_url'])
  
  pd_brand = opn['pd_brand']
  pd_model = opn['pd_model_or_name']
  pd_specs = opn['pd_key_specs']
  pd_info_components = [pd_brand, pd_model, pd_specs]

  # If enough info to search...
  if is_searchable(pd_info_components):
    pd_info_str_extracted = " ".join(filter(None, pd_info_components))
    # Add pd category name to search str if not already inside
    if contains_phrase_or_variants(pd_info_str_extracted, pd_category_name):
      search_str = pd_info_str_extracted
    else:
      search_str = f'{pd_info_str_extracted} {pd_category_name}'
    # Search Amazon
    amzn_results = await search_pd_amzn(search_str, 10)
    if amzn_results:
      matched_item = await match_pd_info(amzn_results, pd_info_str_extracted)
      # If found on Amazon, furnish with asin
      if matched_item and matched_item.asin:
        opn = await process_opn_w_asin(opn, matched_item.asin)

  # If product cannot be identified, and pd_brand was identified, set 'brand_id' according to pd_brand
  if not opn['brand_id'] and pd_brand:
    # Lock to prevent race conditions when checking and adding brands and products
    async with process_opn_w_db_lock:
      brand = await db_add_brand_if_new(pd_brand, opn['pd_category_id'])
      opn['brand_id'] = brand['id']
  
  # If product cannot be identified, and pd_brand was not identified, let brand_id remain as None

  return opn




def is_searchable(pd_info_components: list[str]) -> bool:
  valid_components = [c for c in pd_info_components if c]
  is_searchable = len(valid_components) >= 2
  return is_searchable

async def match_pd_info(amzn_results: list[Item], pd_info_str_extracted: str) -> Optional[Item]:

  amzn_titles = [get_formatted_title(item) for item in amzn_results]
  amzn_titles_indexed = "\n".join(
    f"{i+1}. {title}" for i, title in enumerate(amzn_titles)
  )
  
  current_dir = Path(__file__).parent
  sys_prompt_path = current_dir.parent / "llm_prompts" / "is_amzn_item_match_pd_info_sys.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
  user_prompt = f"Product info string: {pd_info_str_extracted}\n\nAmazon product titles:\n{amzn_titles_indexed}"
  model = "gpt-4o-mini"
  response_format = { "type": "json_object" }

  print(f'\nChecking if any amzn result matches pd info...\n- Pd str extracted: {pd_info_str_extracted}\n')
  openai_response = await get_openai_response(sys_prompt, user_prompt, model, response_format, 'match_pd_info')
  if openai_response and 'match_index' in openai_response:
    match_index = openai_response['match_index']
    if match_index is not None and 0 <= match_index < len(amzn_results):
      matched_item = amzn_results[match_index]
      print(f'-> Match found: {matched_item.item_info.title.display_value}')
      return matched_item
  
  print('-> No match found')
  return None

def get_formatted_title(item: Item) -> str:
  title = "Unknown Title"
  brand = "Unknown Brand"

  if item.item_info and item.item_info.title:
    title = item.item_info.title.display_value

  if (item.item_info and 
      item.item_info.by_line_info and 
      item.item_info.by_line_info.brand):
    brand = item.item_info.by_line_info.brand.display_value

  return f"{title} (Brand: {brand})"


async def add_amzn_item_to_db(amzn_item: Item, pd_category_id: int) -> tuple[int, int, int]:
  brand_name = amzn_item.item_info.by_line_info.brand.display_value if amzn_item.item_info and amzn_item.item_info.by_line_info and amzn_item.item_info.by_line_info.brand else None
  brand = await db_add_brand_if_new(brand_name, pd_category_id)
  brand_id = brand['id']

  pd_data = {
    'asin': amzn_item.asin if amzn_item.asin else None,
    'title': amzn_item.item_info.title.display_value if amzn_item.item_info and amzn_item.item_info.title else None,
    'amzn_url': amzn_item.detail_page_url if amzn_item.detail_page_url else None,
    'amzn_price': amzn_item.offers.listings[0].price.amount if amzn_item.offers and amzn_item.offers.listings and amzn_item.offers.listings[0] and amzn_item.offers.listings[0].price else None,
    'img_url': amzn_item.images.primary.large.url if amzn_item.images and amzn_item.images.primary and amzn_item.images.primary.large else None
  }
  pd = await db_add_pd(pd_data)
  product_id = pd['id']
  
  product_brand = await db_add_product_brand(product_id, brand_id)
  product_brand_id = product_brand['id']
  
  return product_id, brand_id, product_brand_id


async def get_pd_brand(url: str) -> Optional[str]:
  # Search Google using the URL
  search_results = await fetch_google_results(url, "", None, 3)

  # Prepare the search results for LLM input
  search_content = "\n\n".join([f"{i+1}. Title: {item['title']}\nSnippet: {item['snippet']}" for i, item in enumerate(search_results)])
  print(search_content)

  # Prepare prompts for LLM
  current_dir = Path(__file__).parent
  sys_prompt_path = current_dir.parent / "llm_prompts" / "get_pd_brand.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
  user_prompt = f"Product URL: {url}\n\nTop search results for searching the product URL:\n{search_content}"

  # Use LLM to extract the brand
  response = await get_openai_response(sys_prompt, user_prompt, "gpt-4o-mini", { "type": "json_object" }, 'get_pd_brand')

  # Extract and return the brand
  brand = response.get("brand", None)
  return brand


def contains_phrase_or_variants(initial_text: str, phrase: str) -> bool:
  p = inflect.engine()
  words = phrase.lower().split()
  initial_text_lower = initial_text.lower()

  # Check if any word or its variant exists in the initial text
  for word in words:
    singular = p.singular_noun(word) or word
    plural = p.plural(word)
    
    if (singular in initial_text_lower or 
        plural in initial_text_lower):
      return True
    else:
      return False


