from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import cgi
import argparse
from socket import gethostbyname, gethostname

# Define the upload directory
UPLOAD_DIR = "./uploads"

class UploadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML form for file upload
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = """
        <html>
        <head><title>File Upload</title></head>
        <body>
        <h2>Upload a File</h2>
        <form action="/" method="post" enctype="multipart/form-data">
            Username: <input type="text" name="username" required><br><br>
            <input type="file" name="file" required><br><br>
            <input type="submit" value="Upload">
        </form>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        # Parse the form data uploaded
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        # Get the uploaded file and username
        uploaded_file = form['file']
        username = form['username'].value

        # Get client IP address
        client_ip = self.client_address[0]

        # Generate the filename using the template: IP_username_filename
        filename_template = f"{client_ip}_{username}_{uploaded_file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename_template)

        # Save the file to the upload directory
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.file.read())

        # Send response to client
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'File uploaded successfully!')

def run(server_class=HTTPServer, handler_class=UploadHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}...")
    httpd.serve_forever()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Start a file upload server.')
    parser.add_argument('--port', type=int, default=8000, help='Port number (default: 8000)')
    args = parser.parse_args()
    
    # Create the upload directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    run(port=args.port)
