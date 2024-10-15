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
                    <div class="chessboard" id="board-{fen.replace(' ', '_')}"></div>
                    <script>
                        var board = Chessboard('board-{fen.replace(' ', '_')}', {{
                            position: '{fen}'
                        }});
                    </script>
                    '''

        # Replace all FEN code blocks in the HTML
        new_html = fen_pattern.sub(replace_fen, html)

        # Add the necessary CSS and JS for chessboard.js
        new_html += '''
                <link rel="stylesheet" href="https://unpkg.com/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
                <script src="https://unpkg.com/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
                '''

        return new_html