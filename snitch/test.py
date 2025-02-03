content = """
landscape.jpg","type":"resource"}}},"description":null,"contentType":"hvacontentservice:landscapeImageSet","localeString":null,"id":"7a3db536-991f-4f6b-996a-5e59fc69b89a"}}}},"isPreview":false,"displayName":"Werken bij de HvA | draag bij aan een betere toekomst"},"__N_SSP":true},"page":"/[[...route]]","query":{"route":["over-de-hva","werken-bij"]},"buildId":"Yz2dCfm2aMt5BSw-9Ai0f","runtimeConfig":{"NEXT_PUBLIC_GOOGLE_ANALYTICS":"GTM-PS64NB","NEXT_PUBLIC_SITEIMPROVE":"6005396","NEXT_PUBLIC_ADDSEARCH_SITE_KEY":"f173da3e4b63c047388d62c7f32aef11","NEXT_PUBLIC_SCRIBIT_PRO_API":"46a6b5df-117b-4de2-bbf4-d73e5587430c","NEXT_PUBLIC_LIBRARY_ENDPOINT":"https://diensten.uba.uva.nl/com/primo/redirect/?site=HVA\u0026query=","NEXT_PUBLIC_LIBRARY_ADVANCED_SEARCH_URL":"https://lib.hva.nl/discovery/search?vid=31UKB_UAM2_INST:HVA\u0026mode=advanced","COOKIEBOT_API":"dee62cf0-f687-4c14-af2f-dcd33079406a","GOOGLE_MAPS_API":"AIzaSyDRPWsTzZqg-NE9NU8eyqspPTfiFiFuZls","GRAPHQL_HOST":"https://graphql-prd.cms.hva.nl/graphql","BASE_URL":"https://www.hva.nl","BRXM_ORIGINAL":"https://cms-prd.cms.hva.nl","BRXM_ENDPOINT":"https://cms-prd.cms.hva.nl/site/nl/api"
"""

import re

def extract_urls(text):
    """
    Extracts all URLs from a given string.
    """
    url_pattern = re.compile(
        r'https?://[^\s<>"]+|www\.[^\s<>"]+|ftp://[^\s<>"]+|[a-zA-Z]+://[^\s<>"]+'
    )
    return url_pattern.findall(text)

print(extract_urls(content))
