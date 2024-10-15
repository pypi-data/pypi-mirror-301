import re

from mkdocs.plugins import BasePlugin


class ChessboardPlugin(BasePlugin):
    def on_page_markdown(self, markdown, **kwargs):
        # Regular expression to find code blocks starting with ```FEN
        fen_pattern = re.compile(r'```FEN\s+([^`]+)```', re.MULTILINE)

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

        # Replace all FEN code blocks in the markdown
        new_markdown = fen_pattern.sub(replace_fen, markdown)

        # Add the necessary CSS and JS for chessboard.js
        new_markdown += '''
                <link rel="stylesheet" href="https://unpkg.com/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css">
                <script src="https://unpkg.com/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"></script>
                '''

        return new_markdown
