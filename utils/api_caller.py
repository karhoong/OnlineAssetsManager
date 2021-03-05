import urllib


def get_asset_type():
    url = "http://maya.oam-tool.com/get_assets_info.php"
    headers = {}
    post_response = urllib.urlopen(url=url)
    print(post_response.read())