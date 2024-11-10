import serial
from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# HTML template with updated background styling (same as your original)
html = '''
<!DOCTYPE html>
<html lang="en">
<head>  
    <meta charset="UTF-8">
    <title>Sentence Input Form</title>
    <!-- Bootstrap CSS CDN -->
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
    />
    <!-- Custom Styles -->
    <style>
        body {
            background-color: #e0f7fa; /* Slightly teal background */
            background-image: radial-gradient(circle at 20px 20px, rgba(0, 0, 0, 0.02) 2%, transparent 0%), radial-gradient(circle at 0px 0px, rgba(0, 0, 0, 0.02) 2%, transparent 0%);
            background-size: 40px 40px;
            color: #333;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center; /* Center horizontally */
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            padding: 20px;
        }
        .input-container {
            width: 100%;
            max-width: 800px; /* Increased max-width to make the bubble wider */
            padding: 0 20px;
        }
        .input-bubble {
            background-color: rgba(255, 255, 255, 0.85); /* White with slight transparency */
            border: none;
            border-radius: 50px; /* Circular rectangular box */
            box-shadow: 0 10px 30px rgba(0,0,0,0.1); /* Enhanced shadow for separation */
            padding: 20px;
            display: flex;
            align-items: center;
            width: 100%;
        }
        .form-control {
            background-color: rgba(255, 255, 255, 0.9);
            color: #333;
            border: 1px solid #ccc;
            border-radius: 25px; /* More rounded input field */
            padding: 15px;
            flex-grow: 1; /* Allow the input to grow and fill available space */
            margin-right: 10px;
            min-width: 0; /* Prevents the input from overflowing */
        }
        .form-control::placeholder {
            color: #999;
        }
        .form-control:focus {
            background-color: rgba(255, 255, 255, 0.95);
            color: #333;
            border-color: #1a237e; /* Dark blue border on focus */
            box-shadow: 0 0 5px rgba(26, 35, 126, 0.5);
        }
        .btn-custom {
            background-color: #1a237e; /* Dark blue button */
            color: #fff;
            border-radius: 30px; /* Rounded button */
            padding: 12px 20px;
            font-weight: bold;
            border: none;
            flex-shrink: 0; /* Prevent the button from shrinking */
        }
        .btn-custom:hover {
            background-color: #283593; /* Slightly lighter dark blue on hover */
            color: #fff;
        }
        h2 {
            font-weight: bold;
            text-align: center;
            margin-bottom: 30px;
            color: #1a237e; /* Dark blue heading */
        }
    </style>
</head>
<body>

<div class="input-container">
    <h2>BrailleFlow</h2>
    <form action="/submit_sentence" method="post" class="input-bubble">
        <input type="text" class="form-control" name="sentence" placeholder="Enter Text..." required />
        <button type="submit" class="btn btn-custom">Translate</button>
    </form>
</div>

<!-- Bootstrap JS and dependencies -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script
  src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"
></script>
<script
  src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
></script>

</body>
</html>
'''

def get_braille(raw):
    hash_table = {
        'a': '100000',
        'b': '101000',
        'c': '110000',
        'd': '110100',
        'e': '100100',
        'f': '111000',
        'g': '111100',
        'h': '101100',
        'i': '011000',
        'j': '011100',
        'k': '100010',
        'l': '101010',
        'm': '110010',
        'n': '110110',
        'o': '100110',
        'p': '111010',
        'q': '111110',
        'r': '101110',
        's': '011010',
        't': '011110',
        'u': '100011',
        'v': '101011',
        'w': '011101',
        'x': '110011',
        'y': '110111',
        'z': '100111',
        '.': '001101',
        ' ': '000000',
        ',': '001000'
    }
    cooked = raw.lower()
    ret_str = ""

    for char in cooked:
        if char in hash_table:
            ret_str += hash_table[char] + "_"
        else:
            ret_str += '000000_'  # Placeholder for unknown characters

    # Remove trailing underscore
    if ret_str.endswith('_'):
        ret_str = ret_str[:-1]
    
    return ret_str

@app.route('/', methods=['GET'])
def index():
    # Render the HTML form
    return render_template_string(html)

@app.route('/submit_sentence', methods=['POST'])
def submit_sentence():
    # Retrieve the sentence from the form
    sentence_input = request.form['sentence']
    braille_sequence = get_braille(sentence_input)
    
    # Send the braille sequence over serial to the Pico
    try:
        # Replace 'COM8' with your actual COM port (e.g., 'COM3' on Windows or '/dev/ttyACM0' on Linux/Mac)
        ser = serial.Serial('COM8', 115200, timeout=1)
        ser.write((braille_sequence + '\n').encode('utf-8'))  # Send the bit sequence followed by newline
        ser.close()
        print(f"Braille sequence sent successfully: {braille_sequence}")
    except Exception as e:
        print(f"Error sending data over serial: {e}")
    
    # Redirect back to the main page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)