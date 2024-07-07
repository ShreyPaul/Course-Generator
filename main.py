
import openai

import os

from flask import Flask, render_template_string, request

openai.api_key = os.environ['OPENAI_API_KEY']


def generate_tutorial(components):
  response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
          {
              "role": "system",
              "content": "You are a helpful assistant who only provides information about courses, if course name provided seems irrelevant than ask to resubmit with valid name. if the same name is resubmitted then try to generate course information."
          },
          {
              "role": "user",
              "content": "Computer Networks"
          },
          {
              "role": "assistant",
              "content": "Objective of the Course: To provide students with a comprehensive understanding of computer networks, including design, configuration, and troubleshooting, in order to prepare them for careers in networking and related fields. Sample Syllabus: - Introduction to Computer Networks - Network Topologies and Protocols - Network Security and Data Encryption - Network Design and Configuration - Wireless Networks and Mobile Computing - Network Troubleshooting and Maintenance Three Measurable Outcomes: 1. Knowledge: Students will be able to demonstrate an understanding of fundamental networking concepts, protocols, and technologies. 2. Comprehension: Students will be able to analyze and evaluate different network topologies and security measures. 3. Application: Students will be able to design and implement a network infrastructure to meet specific business requirements. Assessment Methods: - Quizzes and exams to assess knowledge and comprehension - Hands-on labs and projects to evaluate application skills - Case studies and presentations to assess problem-solving abilities Recommended Readings and Textbooks: 1. 'Computer Networking: A Top-Down Approach' by James Kurose and Keith Ross 2. 'Computer Networks' by Andrew S. Tanenbaum 3. 'Network Security Essentials' by William Stallings 4. 'TCP/IP Illustrated, Volume 1: The Protocols' by W. Richard Stevens"
          },
          {
              "role": "user",
              "content": "Write me a song"
          },
          {
              "role": "assistant",
              "content": "This AI is not trained to generate music. It is only meant to provide course information. If you feel this is an error and correct course name is provided, please resubmit information."
          },
          {
              "role": "user",
              "content": f"You have to return the follow information given the name of the course which is {components}. Objective of the Course: A concise statement that describes the purpose and goals of the course. Sample Syllabus: An AI-generated syllabus outline that covers the main topics and modules to be taught. Three Measurable Outcomes: Specific, measurable learning outcomes categorized according to Bloom's Taxonomy levels: Knowledge, Comprehension, and Application. Assessment Methods: Suggestions on how to evaluate the learning outcomes through various forms of assessment. Recommended Readings and Textbooks: A list of AI-recommended resources, including books, articles, and other materials relevant to the course content."
          },
      ]
  )
  return response.choices[0].message.content



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])


def hello():
 output = ""
 if request.method == 'POST':
  components = request.form['components']
  output = generate_tutorial(components)

 return render_template_string('''

 <!DOCTYPE html >
 <html >
 <head >
  <title >Infinite Project Generator </title >
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
    rel="stylesheet">
  <script >

  async function generateTutorial() {
   const components = document.querySelector('#components').value;
   const output = document.querySelector('#output');
   output.textContent = 'Fetching information about the course...';
   const response = await fetch('/generate', {
    method: 'POST',
    body: new FormData(document.querySelector('#tutorial-form'))
   });
   const newOutput = await response.text();
   output.textContent = newOutput;
  }
  function copyToClipboard() {
   const output = document.querySelector('#output');
   const textarea = document.createElement('textarea');
   textarea.value = output.textContent;
   document.body.appendChild(textarea);
   textarea.select();
   document.execCommand('copy');
   document.body.removeChild(textarea);
   alert('Copied to clipboard');
  }

  </script >
 </head >
 <body >
  <div class="container">
   <h1 class="my-4" style="text-align:center">Course Information Generator</h1 >
   <form id="tutorial-form" onsubmit="event.preventDefault(); generateTutorial();" class="mb-3">
    <div class="mb-3">
     <label for="components" class="form-label">Course Name:</label >
     <input type="text" class="form-control" id="components" name="components" placeholder="Enter the name of the course you want information for " required >
    </div ><div style = "text-align:center">
    <button type="submit" class="btn btn-primary" >Share the course information with me </button >
    </div>
   </form >
   <div class="card">
    <div class="card-header d-flex justify-content-between align-items-center">
     Output:
     <button class="btn btn-secondary btn-sm" onclick="copyToClipboard()">Copy </button >
    </div >
    <div class="card-body">
     <pre id="output" class="mb-0" style="white-space: pre-wrap;">{{ output }}</pre >
    </div >
   </div >
  </div >
 </body >
 </html >
 ''',
                output=output)



@app.route('/generate', methods=['POST'])

def generate():
 components = request.form['components']
 return generate_tutorial(components)


if __name__ == '__main__':
 app.run(host='0.0.0.0', port=8080)

