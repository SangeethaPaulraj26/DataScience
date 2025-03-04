{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPWSr7p+ejv2u6kwSU1o+4D",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/SangeethaPaulraj26/DataScience/blob/main/script_api.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "id": "tlc7B8ab3Eiv"
      },
      "outputs": [],
      "source": [
        "import json\n",
        "import markdown\n",
        "import requests\n",
        "import re\n",
        "from bs4 import BeautifulSoup\n",
        "from markdown.extensions.toc import TocExtension\n",
        "from markdown.extensions.extra import ExtraExtension\n",
        "\n",
        "def slugify(text):\n",
        "    \"\"\"Convert text to a slug for an HTML id.\"\"\"\n",
        "    text = text.lower().replace('&', 'and')\n",
        "    text = re.sub(r'[^a-z0-9\\s-]', '', text)\n",
        "    text = re.sub(r'\\s+', '-', text)\n",
        "    text = re.sub(r'-+', '-', text)\n",
        "    return text.strip('-')\n",
        "\n",
        "def markdown_to_clean_html(json_string):\n",
        "    \"\"\"Convert Markdown content in JSON to clean HTML with table styling, TOC, and external CSS.\"\"\"\n",
        "    try:\n",
        "        data = json.loads(json_string)\n",
        "        if \"response\" in data:\n",
        "            markdown_content = data[\"response\"]\n",
        "\n",
        "            raw_html = markdown.markdown(\n",
        "                markdown_content,\n",
        "                extensions=[TocExtension(marker=\"<!--TOC-->\"), ExtraExtension()]\n",
        "            )\n",
        "\n",
        "            raw_html = re.sub(r\"<hr\\s*/?>\", \"\", raw_html)\n",
        "            raw_html = raw_html.replace(\"<table>\", '<table class=\"styled-table\">')\n",
        "\n",
        "            soup = BeautifulSoup(raw_html, \"html.parser\")\n",
        "\n",
        "            for tag in soup.find_all(True):\n",
        "                tag.attrs.pop(\"style\", None)\n",
        "\n",
        "            for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):\n",
        "                header_text = header.get_text()\n",
        "                cleaned_text = re.sub(r'^\\d+(\\.\\d+)*\\s*', '', header_text)\n",
        "                header['id'] = slugify(cleaned_text)\n",
        "\n",
        "            toc_list = soup.find('ol')\n",
        "            if toc_list:\n",
        "                for link in toc_list.find_all('a'):\n",
        "                    link_text = link.get_text()\n",
        "                    cleaned_link_text = re.sub(r'^\\d+(\\.\\d+)*\\s*', '', link_text)\n",
        "                    link['href'] = '#' + slugify(cleaned_link_text)\n",
        "\n",
        "                toc_div = soup.new_tag('div', **{'class': 'toc'})\n",
        "                toc_heading = soup.new_tag('h2')\n",
        "                toc_heading.string = 'Table of Contents'\n",
        "                toc_div.append(toc_heading)\n",
        "                toc_div.append(toc_list.extract())\n",
        "\n",
        "                first_h1 = soup.find('h1')\n",
        "                if first_h1:\n",
        "                    first_h1.insert_after(toc_div)\n",
        "                else:\n",
        "                    soup.insert(0, toc_div)\n",
        "\n",
        "            final_html = f'''<!DOCTYPE html>\n",
        "<html lang=\"en\">\n",
        "<head>\n",
        "    <meta charset=\"UTF-8\">\n",
        "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n",
        "    <title>Formatted Report</title>\n",
        "    <link rel=\"stylesheet\" href=\"style1.css\">\n",
        "</head>\n",
        "<body>\n",
        "    {str(soup)}\n",
        "</body>\n",
        "</html>'''\n",
        "\n",
        "            return final_html\n",
        "        else:\n",
        "            return \"Invalid JSON structure: 'response' key missing.\"\n",
        "    except json.JSONDecodeError:\n",
        "        return \"Invalid JSON format.\"\n",
        "\n",
        "# ✅ Updated API URL & Key\n",
        "url = \"https://agent.ai/agent/e8jd2c4lf9ew0ygm\"\n",
        "\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "p2zbwb263SVG"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}