import requests
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TumblrFetcher:
    def __init__(self, blog_name):
        self.blog_name = blog_name
        self.base_url = f"https://{blog_name}.tumblr.com/api/read/json"
    
    def get_data(self, start, end):
        response = requests.get(self.base_url)
        logger.info(response.text)

        #removing 'var tumblr_api_read' prefix
        json_str = response.text.replace('var tumblr_api_read = ', '')[:-2]
        self.blog_info = json.loads(json_str)
        logger.info(json.dumps(self.blog_info, indent=2))
        
        params = {
            'type': 'photo',
            'start': start - 1,
            'num': end - start + 1
        }
        response = requests.get(self.base_url, params=params)
        json_str = response.text.replace('var tumblr_api_read = ', '')[:-2]
        self.posts = json.loads(json_str)
    
    def show_info(self):
        tumblelog = self.blog_info['tumblelog']
        print(f"\ntitle: {tumblelog.get('title', 'N/A')}")
        print(f"name: {tumblelog.get('name', 'N/A')}")
        print(f"description: {tumblelog.get('description', 'N/A')}")
        print(f"no of post: {self.blog_info.get('posts-total', 0)}\n")
        
    def show_images(self, start):
        post_num = start
        for post in self.posts['posts']:
            if 'photo-url-1280' in post:
                print(f"{post_num}. {post['photo-url-1280']}")
            
            if 'photos' in post:
                for photo in post['photos']:
                    print(f"{post_num}. {photo['photo-url-1280']}")
            post_num += 1

def main():
    print("Enter the Tumblr blog name:")
    blog_name = input()

    print("Enter the range:")
    range_input = input()

    range_parts = range_input.split('-')
    start = int(range_parts[0])
    end = int(range_parts[1])

    try:
        fetcher = TumblrFetcher(blog_name)
        fetcher.get_data(start, end)
        fetcher.show_info()
        fetcher.show_images(start)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()