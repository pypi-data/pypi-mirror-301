import re

from mkdocs.plugins import BasePlugin


class ChessboardPlugin(BasePlugin):
    @staticmethod
    def lichess_form(fen: str, stockfish_level: int = 8):
        player = 'white' if fen.split(' ')[1] == 'w' else 'black'

        return f'''
        <form id="form-{fen.replace(' ', '_').replace('/', '_')}" action="https://lichess.org/setup/ai" method="POST" style="display: none;">
                        <input type="hidden" name="fen" value="{fen}">
                        <input type="hidden" name="variant" value="3">
                        <input type="hidden" name="timeMode" value="1">
                        <input type="hidden" name="time" value="3">
                        <input type="hidden" name="time_range" value="7">
                        <input type="hidden" name="increment" value="0">
                        <input type="hidden" name="increment_range" value="0">
                        <input type="hidden" name="days" value="2">
                        <input type="hidden" name="days_range" value="2">
                        <input type="hidden" name="mode" value="0">
                        <input type="hidden" name="ratingRange" value="1305-2305">
                        <input type="hidden" name="ratingRange_range_min" value="-500">
                        <input type="hidden" name="ratingRange_range_max" value="500">
                        <input type="hidden" name="level" value="{stockfish_level}">
                        <input type="hidden" name="color" value="{player}">
                    </form>
                    <a href="#" class="post-link" onclick="document.getElementById('form-{fen.replace(' ', '_').replace('/', '_')}').submit(); return false;">Play against Stockfish level {stockfish_level}</a>
        '''

    def on_page_content(self, html, **kwargs):
        # Regular expression to find code blocks starting with ```FEN
        # fen_pattern = re.compile(r'<pre><span></span><code>\[FEN\s+([^<]+)\]</code></pre>', re.MULTILINE)
        fen_pattern = re.compile('<pre><span><\/span><code>\[FEN ([a-zA-Z0-9\/ -]+)]\s+<\/code><\/pre>', re.MULTILINE)
        def replace_fen(match):
            fen = match.group(1).strip()
            player = 'white' if fen.split(' ')[1] == 'w' else 'black'

            return f'''
                    <div class="chessboard" id="board-{fen.replace(' ', '_').replace('/', '_')}"></div>
                    <script>
                        var board = Chessboard('board-{fen.replace(' ', '_').replace('/', '_')}', {{
                            position: '{fen}',
                            orientation: '{player}',
                            pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{'{piece}.png'}'
                        }});
                    </script>
                    {self.lichess_form(fen, 7)}
                    <br>
                    {self.lichess_form(fen, 8)}
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