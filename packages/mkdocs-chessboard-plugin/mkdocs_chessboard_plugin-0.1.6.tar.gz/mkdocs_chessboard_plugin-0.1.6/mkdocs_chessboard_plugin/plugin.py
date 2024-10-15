import re

from mkdocs.plugins import BasePlugin


class ChessboardPlugin(BasePlugin):
    def on_page_content(self, html, **kwargs):
        # Regular expression to find code blocks starting with ```FEN
        # fen_pattern = re.compile(r'<pre><span></span><code>\[FEN\s+([^<]+)\]</code></pre>', re.MULTILINE)
        fen_pattern = re.compile('<pre><span><\/span><code>\[FEN ([a-zA-Z0-9\/ -]+)]\s+<\/code><\/pre>', re.MULTILINE)
        def replace_fen(match):
            fen = match.group(1).strip()
            return f'''
                    <div class="chessboard" id="board-{fen.replace(' ', '_').replace('/', '_')}"></div>
                    <script>
                        var board = Chessboard('board-{fen.replace(' ', '_').replace('/', '_')}', {{
                            position: '{fen}',
                            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{'{piece}.png'}'
                        }});
                    </script>
                    '''

        # Replace all FEN code blocks in the HTML
        new_html = fen_pattern.sub(replace_fen, html)

        # Add the necessary CSS and JS for chessboard.js
        new_html = '''
                <link rel="stylesheet" href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css" integrity="sha384-q94+BZtLrkL1/ohfjR8c6L+A6qzNH9R2hBLwyoAfu3i/WCvQjzL2RQJ3uNHDISdU" crossorigin="anonymous">
                <script src="https://code.jquery.com/jquery-3.7.1.min.js" integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo=" crossorigin="anonymous"></script>
                <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js" integrity="sha384-8Vi8VHwn3vjQ9eUHUxex3JSN/NFqUg3QbPyX8kWyb93+8AC/pPWTzj+nHtbC5bxD" crossorigin="anonymous"></script>

                ''' + new_html

        return new_html