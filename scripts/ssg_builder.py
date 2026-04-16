# ssg_builder.py

from html import escape
import csv

def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def generate_html(data):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOP STORIES / EXCLUSIVE</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .story {
            margin-bottom: 20px;
        }
        iframe {
            width: 100%;
            height: 360px;
        }
    </style>
</head>
<body>
    """
    
    for item in data:
        html_content += f"""
        <div class="story">
            <h2>{escape(item['title'])}</h2>
            <iframe src="{escape(item['youtube_link'])}" frameborder="0"></iframe>
            <p>{escape(item['content'])}</p>
        </div>
        """
    
    html_content += """
</body>
</html>
"""
    return html_content

def main():
    data = read_csv('/Volumes/KIOXIA/clippeaks/scripts/master_data.csv')
    html_content = generate_html(data)
    with open('/Volumes/KIOXIA/clippeaks/public/index.html', mode='w', encoding='utf-8') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()