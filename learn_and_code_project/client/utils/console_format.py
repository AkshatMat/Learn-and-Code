def print_article_list(articles):
    if not articles:
        print("No articles found.")
        return

    for idx, article in enumerate(articles, 1):
        print(f"\n[{idx}] {article.get('title', 'No Title')}")
        print(f"   ID      : {article.get('uuid', 'N/A')}")
        print(f"   Date    : {article.get('published_at', 'Unknown')}")
        print(f"   Category: {article.get('category', 'Uncategorized')}")
        print(f"   Source  : {article.get('source', 'Unknown')}")
        print(f"   URL     : {article.get('url', 'No URL')}")
        print(f"   Content :\n {article.get('content', 'No content available')}")
        print(f"\n Author :\n {article.get('author', 'Unknown')}")
