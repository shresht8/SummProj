#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 10:15:08 2023

@author: shreshtshetty
"""

p0_prompt_template = """You are an AI that summarises the first page of a transcript.

Your job is to summarise the first page of the document, and make notes using text\
elements such as title, headings, sub-headings, bullet points etc. User other page elements if more appropriate.\
Output the text in HTML format. Use the following instructions for preprocessing and summarising:

-Identify the type of transcript it is: It can be a seminar, podcast, tutorial, summit,\
lecture etc. It may involve just one person or could involve multiple people.
-Summarise content in the most optimal manner based on the type of transcript.
-Don't conclude the the summary as it will be appended by the summary of the next page.
-Summary should include page elements Title, Headings, sub-headings and content withing these page elements.
-Content within page elements should be descriptive as readers need to understand context. Use bullet points, numbered\
lists etc only when needed.
- Ignore irrelevant parts of the text: The irrelevant parts can be random text in the middle \
of a sentence (they don’t make sense in context of the sentence)


Page 1 of a 30 page transcript:
{text}

HTML output of page 1:

"""

json_prompt_template = """You are an AI that creates a JSON which represents the summary structure in it. 
You will receive HTML text as input. Use the instructions below to extract items from the HTML text and create 
a JSON output out of it:

Use the following instructions to create your JSON output which represents the structure of the HTML file:
- Output JSON needs to be in a hierarchical manner representing parent-child relationship. For instance a parent\
heading may have multiple headings under it. So you must make that parent heading as key and all its children headings\
as values in the JSON.
- Only title and different headings are to be included in the JSON. Any descriptive content, bullet points, numbered\
lists etc are not to be included,
- For each of the elements in the JSON, one of the value has to be the page number.

Use the example JSON structure as a reference to create your JSON. You dont have to create this exact JSON structure.\
Given example is to highlight hierarchy in JSON, key-value pairs. Form the output JSON according to the elements in \
your HTML output

HTML text of page :

<h1>Bryce Hoffman WBECS 2022 Full Summit Transcript</h1>
<h2>Live Session Date: Thursday, October 27, 2022</h2>
<h3>Session Title: Red Team Thinking® for Coaches</h3>
<p>Lissa Qualls welcomed the audience and introduced the mission of WBECS by Coaching.com. She also mentioned the implementation mastery session related to today's presentation. </p>
<p>Bryce Hoffman, president of Red Team Thinking, is passionate about helping others to bolster their business against disruptions through stress testing strategies, identifying missed opportunities, and much more. He will talk about three things: what Red Team Thinking is, where it comes from and the science and psychology behind it, and how coaches can start using a little bit of Red Team Thinking right away with their clients. </p>

JSON output:
{{
  "Bryce Hoffman WBECS 2022 Full Summit Transcript": {{
    "Page": 1,
    "Type": "h1",
    "Live Session Date: Thursday, October 27, 2022": {{
      "Page": 1,
      "Type": "h2",
      "Session Title: Red Team Thinking® for Coaches": {{
        "Page": 1,
        "Type": "h3"
      }}
    }}
  }}
}}

HTML text of page 1:
{text}

JSON output:


"""

raw_text_template = """Your job is to paraphrase the last 4 sentences of the text given. Include as much \
information as possible. If more context provides a better summary then use remaining text as context. 

Page transcript:
{text}
"""

refine_template = ("""
You are an AI that summarises the given page of a transcript.

Your job is to summarise the page 2 of the document, and make notes using text\
elements such as headings, sub-headings, bullet points etc. User other page elements if more appropriate.\
Output the text in HTML format. Use the following instructions for preprocessing and summarising

Output the text in HTML format. Use the following instructions for preprocessing and summarising:

-Create the HTML summary only based on content in page 2. Do not include any content apart from the content in page 2.
-HTML summary of page 2 should be a continuation of HTML summary of page 1
-Content within page elements should be descriptive as readers need to understand context. Use bullet points, numbered\
lists etc only when needed.
- Ignore irrelevant parts of the text: The irrelevant parts can be random text in the \
middle of a sentence (they don’t make sense in context of the sentence)

You have access to 3 contextual data that will help you create your summary of the given page. Do not use the contextual\
information in your final output. Your final output must contain content from the given page to be summarised.

The last 3 sentences from the raw transcript of the page 1 will help you get context of the start of \
the given page since the start of the given age may be part of an unfinished sentence from the previous page.
last 3 sentences of the page 1: {raw_text_latest}

Table of contents of all title,headings, sub-headings from previous page will give you context of all the content \
before given page to summarise. 
JSON document structure of past summaries: {json}

Page 1 summarised HTML will help you understand context of the content in the previous page as the content to be summarised\
in page 2 is the continuation of the page 1. Do not include page 2 summarised HTML in the output, you must only\
use it as context to create a HTML summary of page 2.
Previous page HTML: {previous_page_HTML}


Page 2 of 30 page transcript(Summarise content of this page only, do not include previous page information): {page}


HTML output of page 2:

""")


json_prompt_template_p1 = """You are an AI that adds headings, sub-headings from the HTML text you receive as input
into the JSON table of contents

Use the following instructions to create your JSON output which represents the structure of the HTML file:

- Output JSON needs to be in a hierarchical manner representing parent-child relationship. For instance a parent\
heading may have multiple headings under it. So you must make that parent heading as key and all its children headings\
as values in the JSON.
- Only title and different headings are to be included in the JSON. Any descriptive content, bullet points, numbered\
lists etc are not to be included,
- For each of the elements in the JSON, one of the value has to be the page number.

Use the example to understand how to add headings and sub-headings from the HTML text into the JSON table of \
contents.

HTML text of page :

<h3>What is Red Team Thinking?</h3>
<p>Red Team Thinking is a cognitive capability designed to engage critical thinking, expose unseen threats and missed opportunities. It is designed to enable distributed decision making, helping leaders drive decision making as close to the coalface as possible. It also encourages diversity of thought, so that the best idea can win regardless of where it comes from inside the organization. Red Team Thinking is both a mindset and a set of tools. The tools are designed to help navigate complexity, think more strategically, develop new ideas and perspectives, create plans with optionality in them that are more adaptive and resilient, and to make better decisions faster. The mindset is about looking at the world differently and taking a hard unflinching look at the challenges and opportunities. It is aimed at developing the three Cs: Clarity, Capability and Commitment.</p>

JSON table of contents (input):
{{
  "Bryce Hoffman WBECS 2022 Full Summit Transcript": {{
    "Page": 1,
    "Type": "h1",
    "Live Session Date: Thursday, October 27, 2022": {{
      "Page": 1,
      "Type": "h2",
      "Session Title: Red Team Thinking® for Coaches": {{
        "Page": 1,
        "Type": "h3"
      }}
    }}
  }}
}}

JSON table of contents (output):
{{
  "Bryce Hoffman WBECS 2022 Full Summit Transcript": {{
    "Page": 1,
    "Type": "h1",
    "Live Session Date: Thursday, October 27, 2022": {{
      "Page": 1,
      "Type": "h2",
      "Session Title: Red Team Thinking® for Coaches": {{
        "Page": 1,
        "Type": "h3"
      }},
      "What is Red Team Thinking?":{{
        "Page": 2,
        "Type": "h3"
      }}
    }}
  }}
}}

HTML text of page 2:
{text}

JSON table of contents:
{json}

JSON table of contents (output):


"""
