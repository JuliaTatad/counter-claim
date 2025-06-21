import markdown
import os

def create_html_report():
    """
    Reads report.md, converts it to HTML, and applies custom CSS for a
    beautiful, aesthetically pleasing output.
    """
    try:
        with open("report.md", "r", encoding="utf-8") as f:
            md_content = f.read()
    except FileNotFoundError:
        print("Error: report.md not found.")
        return

    # Convert markdown to HTML, enabling the 'tables' extension
    html_body = markdown.markdown(md_content, extensions=['tables'])

    # Define the CSS for styling the report
    css_style = """
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #343a40;
        background-color: #f8f9fa;
        margin: 0;
        padding: 20px;
    }
    .container {
        max-width: 850px;
        margin: 0 auto;
        background-color: #ffffff;
        padding: 40px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    h1, h2, h3, h4, h5, h6 {
        color: #0056b3;
        font-weight: 600;
        border-bottom: 2px solid #e9ecef;
        padding-bottom: 10px;
        margin-top: 1.5em;
    }
    h1 { font-size: 2.2em; }
    h2 { font-size: 1.8em; }
    h3 { font-size: 1.5em; }
    h4 { font-size: 1.2em; border-bottom: 1px solid #e9ecef; }
    p {
        margin-bottom: 1.2em;
    }
    a {
        color: #007bff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.5em;
        margin-bottom: 1.5em;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    th, td {
        padding: 12px 15px;
        border: 1px solid #dee2e6;
        text-align: left;
    }
    th {
        background-color: #f2f2f2;
        font-weight: bold;
        color: #495057;
    }
    tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    tr:hover {
        background-color: #e9ecef;
    }
    blockquote {
        border-left: 5px solid #007bff;
        padding: 15px 20px;
        margin: 25px 0;
        background-color: #f1f8ff;
        color: #333;
        font-style: italic;
    }
    code {
        background-color: #e9ecef;
        padding: 3px 5px;
        border-radius: 4px;
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
    }
    hr {
        border: 0;
        height: 1px;
        background: #dee2e6;
        margin: 2.5em 0;
    }
    """

    # Combine into a full HTML document
    full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Strategic Analysis Report</title>
    <style>
        {css_style}
    </style>
</head>
<body>
    <div class="container">
        {html_body}
    </div>
</body>
</html>
    """

    # Write the HTML to a file
    try:
        with open("report.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Successfully generated report.html")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    create_html_report()
