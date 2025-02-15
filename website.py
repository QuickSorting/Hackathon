neovim_mermaid =  """
flowchart TD
node0["test_makeencoding.py: set_output_encoding"]
node1["test_makeencoding.py: main"]
node2["test_makeencoding.py: get_text_writer"]
node3["test_makeencoding.py: convwrite"]
node4["nvim-gdb-pretty-printers.py: get_color_code"]
node5["nvim-gdb-pretty-printers.py: highlight"]
node6["nvim-gdb-pretty-printers.py: pretty_printers"]
node7["nvim-gdb-pretty-printers.py: __init__"]
node8["nvim-gdb-pretty-printers.py: to_string"]
node9["nvim-gdb-pretty-printers.py: display_hint"]
node10["shadacat.py: strtrans_errors"]
node11["shadacat.py: idfunc"]
node12["shadacat.py: mnormalize"]
node13["shadacat.py: __repr__"]
node14["shadacat.py: filt"]
node15["shadacat.py: __init__"]
node16["clint.py: ParseNolintSuppressions"]
node17["clint.py: ParseKnownErrorSuppressions"]
node18["clint.py: ResetNolintSuppressions"]
node19["clint.py: ResetKnownErrorSuppressions"]
node20["clint.py: IsErrorSuppressedByNolint"]
node21["clint.py: IsErrorInSuppressedErrorsList"]
node22["clint.py: Match"]
node23["clint.py: Search"]
node24["clint.py: _OutputFormat"]
node25["clint.py: _SetOutputFormat"]
node26["clint.py: _VerboseLevel"]
node27["clint.py: _SetVerboseLevel"]
node28["clint.py: _SetCountingStyle"]
node29["clint.py: _SuppressErrorsFrom"]
node30["clint.py: _RecordErrorsTo"]
node31["clint.py: _Filters"]
node32["clint.py: _SetFilters"]
node33["clint.py: _ShouldPrintError"]
node34["clint.py: Error"]
node35["clint.py: IsCppString"]
node36["clint.py: FindNextMultiLineCommentStart"]
node37["clint.py: FindNextMultiLineCommentEnd"]
node38["clint.py: RemoveMultiLineCommentsFromRange"]
node39["clint.py: RemoveMultiLineComments"]
node40["clint.py: CleanseComments"]
node41["clint.py: FindEndOfExpressionInLine"]
node42["clint.py: CloseExpression"]
node43["clint.py: CheckForHeaderGuard"]
node44["clint.py: CheckIncludes"]
node45["clint.py: CheckNonSymbols"]
node46["clint.py: CheckForBadCharacters"]
node47["clint.py: CheckForMultilineCommentsAndStrings"]
node48["clint.py: CheckForOldStyleComments"]
node49["clint.py: CheckPosixThreading"]
node50["clint.py: CheckMemoryFunctions"]
node51["clint.py: CheckOSFunctions"]
node52["clint.py: CheckForNonStandardConstructs"]
node53["clint.py: IsBlankLine"]
node54["clint.py: CheckComment"]
node55["clint.py: FindNextMatchingAngleBracket"]
node56["clint.py: FindPreviousMatchingAngleBracket"]
node57["clint.py: CheckSpacing"]
node58["clint.py: GetPreviousNonBlankLine"]
node59["clint.py: CheckBraces"]
node60["clint.py: CheckStyle"]
node61["clint.py: _GetTextInside"]
node62["clint.py: CheckLanguage"]
node63["clint.py: ProcessLine"]
node64["clint.py: ProcessFileData"]
node65["clint.py: ProcessFile"]
node66["clint.py: PrintUsage"]
node67["clint.py: PrintCategories"]
node68["clint.py: ParseArguments"]
node69["clint.py: main"]
node70["clint.py: __init__"]
node71["clint.py: SetOutputFormat"]
node72["clint.py: SetVerboseLevel"]
node73["clint.py: SetCountingStyle"]
node74["clint.py: SetFilters"]
node75["clint.py: ResetErrorCounts"]
node76["clint.py: IncrementErrorCount"]
node77["clint.py: PrintErrorCounts"]
node78["clint.py: SuppressErrorsFrom"]
node79["clint.py: RecordErrorsTo"]
node80["clint.py: FullName"]
node81["clint.py: RelativePath"]
node82["clint.py: NumLines"]
node83["clint.py: _CollapseStrings"]
node84["clint.py: SeenOpenBrace"]
node85["clint.py: UpdatePreprocessor"]
node86["clint.py: Update"]
node87["clint.py: RecordedError"]
node0 --> node2
node0 --> node2
node1 --> node0
node5 --> node4
node5 --> node4
node8 --> node5
node13 --> node13
node25 --> node71
node27 --> node72
node28 --> node73
node29 --> node78
node30 --> node79
node32 --> node74
node33 --> node20
node33 --> node21
node33 --> node31
node34 --> node33
node34 --> node76
node39 --> node36
node39 --> node37
node39 --> node38
node40 --> node35
node42 --> node82
node42 --> node41
node42 --> node82
node42 --> node41
node42 --> node82
node43 --> node81
node44 --> node81
node44 --> node22
node52 --> node23
node52 --> node23
node52 --> node23
node52 --> node23
node52 --> node22
node55 --> node23
node56 --> node23
node57 --> node53
node57 --> node22
node57 --> node22
node57 --> node22
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node54
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node22
node57 --> node23
node57 --> node55
node57 --> node23
node57 --> node56
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node22
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node57 --> node23
node58 --> node53
node59 --> node22
node59 --> node58
node59 --> node23
node59 --> node22
node59 --> node22
node59 --> node42
node59 --> node22
node60 --> node59
node60 --> node57
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node61
node62 --> node22
node62 --> node23
node62 --> node22
node62 --> node22
node62 --> node23
node62 --> node23
node62 --> node22
node62 --> node22
node62 --> node22
node62 --> node22
node62 --> node22
node62 --> node23
node62 --> node23
node62 --> node23
node62 --> node22
node62 --> node23
node62 --> node41
node63 --> node16
node63 --> node86
node63 --> node47
node63 --> node48
node63 --> node60
node63 --> node62
node63 --> node52
node63 --> node49
node63 --> node50
node63 --> node51
node64 --> node18
node64 --> node19
node64 --> node17
node64 --> node20
node64 --> node34
node64 --> node39
node64 --> node82
node64 --> node63
node64 --> node43
node64 --> node44
node64 --> node45
node64 --> node46
node65 --> node27
node65 --> node64
node68 --> node66
node68 --> node26
node68 --> node24
node68 --> node66
node68 --> node66
node68 --> node67
node68 --> node66
node68 --> node66
node68 --> node66
node68 --> node66
node68 --> node25
node68 --> node27
node68 --> node32
node68 --> node28
node68 --> node29
node68 --> node30
node69 --> node68
node69 --> node75
node69 --> node65
node69 --> node77
node81 --> node80
node85 --> node22
node85 --> node22
node85 --> node22
node86 --> node85
node86 --> node22
node86 --> node84
node86 --> node84
node87 --> node20
node87 --> node34
"""

from flask import Flask, render_template_string

app = Flask(__name__)

def get_mermaid_diagram():
    # Define your Mermaid diagram.
    # Note: Each node is given a unique ID (A, B, C) and a click directive
    # that calls the JavaScript function `expandNode(nodeId)`.
    diagram = neovim_mermaid
    return diagram

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
          <!-- Details injected on node click -->
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
    diagram = get_mermaid_diagram()
    return render_template_string(HTML_TEMPLATE, diagram=diagram)

if __name__ == '__main__':
    app.run(debug=True)
