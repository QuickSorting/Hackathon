import sys
from flask import Flask, render_template_string
from repo_analyzer import RepoAnalyzer

app = Flask(__name__)
diagram = ""

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Interactive Mermaid Diagram</title>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Mermaid JS (with loose security to allow javascript: URLs) -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({startOnLoad:true, securityLevel: 'loose'});
    
    // Function to be called when a node is clicked.
    function expandNode(nodeId) {
      // Details for each node can be fetched dynamically if needed.
      const details = {
        'A': "This is the Start node. You might show an overview of the process here.",
        'B': "This is Process 1. More detailed steps, metrics, or logs could be displayed.",
        'C': "This is the End node. Include summaries, outcomes, or links to further info."
      };
      const content = details[nodeId] || "No details available for this node.";
      
      // Set the modal content and display the modal.
      document.getElementById('modalBody').innerText = content;
      const myModal = new bootstrap.Modal(document.getElementById('detailModal'));
      myModal.show();
    }
  </script>
  <style>
    body {
      background-color: #f7f9fc;
      font-family: 'Roboto', sans-serif;
      padding-top: 40px;
    }
    .mermaid {
      background-color: #fff;
      border: 1px solid #e1e4e8;
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      margin: 20px 0;
    }
    h1 {
      font-weight: 600;
      margin-bottom: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1 class="text-center">Interactive Mermaid Diagram</h1>
    <div class="mermaid">
      {{ diagram | safe }}
    </div>
  </div>

  <!-- Modal for displaying expanded node details -->
  <div class="modal fade" id="detailModal" tabindex="-1" aria-labelledby="detailModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="detailModalLabel">Node Details</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body" id="modalBody">
          <!-- Details injected on noegenerate_mermaide click -->
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Bootstrap JS and dependencies -->
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.6/dist/umd/popper.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, diagram=diagram)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze_repo.py /path/to/repo")
        sys.exit(1)

    repo_path = sys.argv[1]
    analyzer = RepoAnalyzer(repo_path)

    analysis = analyzer.analyze_repository()
    diagram = analyzer.generate_mermaid(analysis)

    print(diagram)

    app.run(debug=True)
