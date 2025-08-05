class AdvancedCaroGame {
    constructor() {
        this.gameSettings = {
            boardSize: 5,
            winCondition: 5,
            gameMode: 'human', // 'human' or 'ai'
            aiDifficulty: 'medium', // 'easy', 'medium', 'hard'
            theme: 'default' // 'default', 'dark', 'colorful'
        };
        
        this.gameState = {
            board: [],
            currentPlayer: 'X',
            gameActive: false,
            score: { X: 0, O: 0 },
            moveHistory: [],
            isAITurn: false
        };
        
        this.screens = {
            menu: document.getElementById('menu-screen'),
            settings: document.getElementById('settings-screen'),
            game: document.getElementById('game-screen'),
            about: document.getElementById('about-screen')
        };
        
        this.loadSettings();
        this.initializeEventListeners();
        this.showScreen('menu');
    }
    
    // ===== INITIALIZATION =====
    initializeEventListeners() {
        // Menu buttons
        document.getElementById('play-vs-human').addEventListener('click', () => this.startGame('human'));
        document.getElementById('play-vs-ai').addEventListener('click', () => this.startGame('ai'));
        document.getElementById('settings-btn').addEventListener('click', () => this.showScreen('settings'));
        document.getElementById('about-btn').addEventListener('click', () => this.showScreen('about'));
        
        // Settings
        document.getElementById('save-settings').addEventListener('click', () => this.saveSettings());
        document.getElementById('back-to-menu').addEventListener('click', () => this.showScreen('menu'));
        
        // Game controls
        document.getElementById('back-to-menu-game').addEventListener('click', () => this.showScreen('menu'));
        document.getElementById('settings-in-game').addEventListener('click', () => this.showScreen('settings'));
        document.getElementById('reset-btn').addEventListener('click', () => this.resetGame());
        document.getElementById('new-game-btn').addEventListener('click', () => this.newGame());
        document.getElementById('hint-btn').addEventListener('click', () => this.showHint());
        document.getElementById('undo-btn').addEventListener('click', () => this.undoMove());
        
        // About
        document.getElementById('back-from-about').addEventListener('click', () => this.showScreen('menu'));
        
        // Modal
        document.getElementById('play-again-btn').addEventListener('click', () => {
            this.closeModal();
            this.resetGame();
        });
        document.getElementById('back-to-menu-modal').addEventListener('click', () => {
            this.closeModal();
            this.showScreen('menu');
        });
        document.getElementById('close-modal-btn').addEventListener('click', () => this.closeModal());
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Settings change listeners
        document.getElementById('board-size').addEventListener('change', (e) => {
            const size = parseInt(e.target.value);
            const winCondition = document.getElementById('win-condition');
            winCondition.innerHTML = '';
            for (let i = 3; i <= Math.min(size, 6); i++) {
                const option = document.createElement('option');
                option.value = i;
                option.textContent = `${i} quân`;
                if (i === Math.min(5, size)) option.selected = true;
                winCondition.appendChild(option);
            }
        });
    }
    
    // ===== SCREEN MANAGEMENT =====
    showScreen(screenName) {
        Object.values(this.screens).forEach(screen => screen.classList.add('hidden'));
        this.screens[screenName].classList.remove('hidden');
        
        if (screenName === 'settings') {
            this.loadSettingsToForm();
        }
    }
    
    // ===== SETTINGS MANAGEMENT =====
    loadSettings() {
        const saved = localStorage.getItem('caroGameSettings');
        if (saved) {
            this.gameSettings = { ...this.gameSettings, ...JSON.parse(saved) };
        }
        this.applyTheme();
    }
    
    saveSettings() {
        this.gameSettings.boardSize = parseInt(document.getElementById('board-size').value);
        this.gameSettings.winCondition = parseInt(document.getElementById('win-condition').value);
        this.gameSettings.aiDifficulty = document.getElementById('ai-difficulty').value;
        this.gameSettings.theme = document.getElementById('game-theme').value;
        
        localStorage.setItem('caroGameSettings', JSON.stringify(this.gameSettings));
        this.applyTheme();
        this.showNotification('Cài đặt đã được lưu!', 'success');
        
        // Nếu đang trong game, tạo lại board
        if (this.gameState.gameActive) {
            this.createBoard();
        }
    }
    
    loadSettingsToForm() {
        document.getElementById('board-size').value = this.gameSettings.boardSize;
        document.getElementById('win-condition').value = this.gameSettings.winCondition;
        document.getElementById('ai-difficulty').value = this.gameSettings.aiDifficulty;
        document.getElementById('game-theme').value = this.gameSettings.theme;
        
        // Trigger board size change to update win condition options
        document.getElementById('board-size').dispatchEvent(new Event('change'));
        document.getElementById('win-condition').value = this.gameSettings.winCondition;
    }
    
    applyTheme() {
        document.body.className = '';
        if (this.gameSettings.theme === 'dark') {
            document.body.classList.add('dark-theme');
        } else if (this.gameSettings.theme === 'colorful') {
            document.body.classList.add('colorful-theme');
        }
    }
    
    // ===== GAME LOGIC =====
    startGame(mode) {
        this.gameSettings.gameMode = mode;
        this.initializeGame();
        this.showScreen('game');
        
        // Update UI
        const modeDisplay = document.getElementById('game-mode-display');
        modeDisplay.textContent = mode === 'ai' ? '🤖 Chơi với máy' : '👥 Hai người chơi';
        
        const playerOName = document.getElementById('player-o-name');
        playerOName.textContent = mode === 'ai' ? '🤖 Máy tính:' : 'Người chơi O:';
        
        document.getElementById('hint-btn').style.display = mode === 'ai' ? 'inline-block' : 'none';
    }
    
    initializeGame() {
        const size = this.gameSettings.boardSize;
        this.gameState.board = Array(size).fill().map(() => Array(size).fill(''));
        this.gameState.currentPlayer = 'X';
        this.gameState.gameActive = true;
        this.gameState.moveHistory = [];
        this.gameState.isAITurn = false;
        
        this.createBoard();
        this.updateDisplay();
        this.updateGameStatus('');
    }
    
    createBoard() {
        const boardElement = document.getElementById('game-board');
        const size = this.gameSettings.boardSize;
        
        // Clear existing board
        boardElement.innerHTML = '';
        boardElement.className = `game-board size-${size}`;
        
        // Create cells
        for (let i = 0; i < size * size; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.dataset.row = Math.floor(i / size);
            cell.dataset.col = i % size;
            cell.addEventListener('click', () => this.handleCellClick(Math.floor(i / size), i % size));
            boardElement.appendChild(cell);
        }
    }
    
    handleCellClick(row, col) {
        if (!this.gameState.gameActive || 
            this.gameState.board[row][col] !== '' || 
            this.gameState.isAITurn) {
            return;
        }
        
        this.makeMove(row, col, this.gameState.currentPlayer);
    }
    
    makeMove(row, col, player) {
        // Record move
        this.gameState.board[row][col] = player;
        this.gameState.moveHistory.push({ row, col, player });
        
        // Update UI
        this.updateCellDisplay(row, col, player);
        
        // Check for win or draw
        if (this.checkWinner(row, col, player)) {
            this.handleGameEnd('win', player);
            return;
        }
        
        if (this.checkDraw()) {
            this.handleGameEnd('draw');
            return;
        }
        
        // Switch player
        this.switchPlayer();
        
        // AI move if needed
        if (this.gameSettings.gameMode === 'ai' && this.gameState.currentPlayer === 'O') {
            this.gameState.isAITurn = true;
            setTimeout(() => this.makeAIMove(), 500);
        }
    }
    
    makeAIMove() {
        if (!this.gameState.gameActive) return;
        
        let move;
        switch (this.gameSettings.aiDifficulty) {
            case 'easy':
                move = this.getRandomMove();
                break;
            case 'medium':
                move = this.getMediumAIMove();
                break;
            case 'hard':
                move = this.getHardAIMove();
                break;
        }
        
        if (move) {
            this.gameState.isAITurn = false;
            this.makeMove(move.row, move.col, 'O');
        }
    }
    
    // ===== AI ALGORITHMS =====
    getRandomMove() {
        const moves = this.getAvailableMoves();
        return moves[Math.floor(Math.random() * moves.length)];
    }
    
    getMediumAIMove() {
        // Check for winning move
        let move = this.findWinningMove('O');
        if (move) return move;
        
        // Block player's winning move
        move = this.findWinningMove('X');
        if (move) return move;
        
        // Take center if available
        const center = Math.floor(this.gameSettings.boardSize / 2);
        if (this.gameState.board[center][center] === '') {
            return { row: center, col: center };
        }
        
        // Random move
        return this.getRandomMove();
    }
    
    getHardAIMove() {
        // Minimax algorithm with alpha-beta pruning
        const depth = this.gameSettings.boardSize <= 5 ? 4 : 3;
        const result = this.minimax(this.gameState.board, depth, -Infinity, Infinity, true);
        return result.move;
    }
    
    minimax(board, depth, alpha, beta, isMaximizing) {
        const score = this.evaluateBoard(board);
        
        if (depth === 0 || Math.abs(score) > 1000) {
            return { score };
        }
        
        const moves = this.getAvailableMovesFromBoard(board);
        if (moves.length === 0) {
            return { score: 0 };
        }
        
        let bestMove;
        
        if (isMaximizing) {
            let maxScore = -Infinity;
            for (const move of moves) {
                board[move.row][move.col] = 'O';
                const result = this.minimax(board, depth - 1, alpha, beta, false);
                board[move.row][move.col] = '';
                
                if (result.score > maxScore) {
                    maxScore = result.score;
                    bestMove = move;
                }
                
                alpha = Math.max(alpha, result.score);
                if (beta <= alpha) break;
            }
            return { score: maxScore, move: bestMove };
        } else {
            let minScore = Infinity;
            for (const move of moves) {
                board[move.row][move.col] = 'X';
                const result = this.minimax(board, depth - 1, alpha, beta, true);
                board[move.row][move.col] = '';
                
                if (result.score < minScore) {
                    minScore = result.score;
                    bestMove = move;
                }
                
                beta = Math.min(beta, result.score);
                if (beta <= alpha) break;
            }
            return { score: minScore, move: bestMove };
        }
    }
    
    evaluateBoard(board) {
        let score = 0;
        const size = this.gameSettings.boardSize;
        const winCondition = this.gameSettings.winCondition;
        
        // Check all possible lines
        for (let row = 0; row < size; row++) {
            for (let col = 0; col < size; col++) {
                if (board[row][col] !== '') continue;
                
                // Check horizontal, vertical, and diagonal lines
                const directions = [[0, 1], [1, 0], [1, 1], [1, -1]];
                for (const [dr, dc] of directions) {
                    score += this.evaluateLine(board, row, col, dr, dc, winCondition);
                }
            }
        }
        
        return score;
    }
    
    evaluateLine(board, startRow, startCol, dr, dc, winCondition) {
        const size = this.gameSettings.boardSize;
        let score = 0;
        
        for (let len = winCondition; len >= 3; len--) {
            for (let offset = 0; offset <= winCondition - len; offset++) {
                let oCount = 0, xCount = 0, empty = 0;
                
                for (let i = 0; i < len; i++) {
                    const r = startRow + (offset + i) * dr;
                    const c = startCol + (offset + i) * dc;
                    
                    if (r < 0 || r >= size || c < 0 || c >= size) break;
                    
                    if (board[r][c] === 'O') oCount++;
                    else if (board[r][c] === 'X') xCount++;
                    else empty++;
                }
                
                if (oCount > 0 && xCount > 0) continue; // Mixed line
                
                if (oCount === len) return 10000; // AI wins
                if (xCount === len) return -10000; // Player wins
                
                if (oCount > 0) score += Math.pow(10, oCount);
                if (xCount > 0) score -= Math.pow(10, xCount);
            }
        }
        
        return score;
    }
    
    findWinningMove(player) {
        const moves = this.getAvailableMoves();
        for (const move of moves) {
            this.gameState.board[move.row][move.col] = player;
            if (this.checkWinner(move.row, move.col, player)) {
                this.gameState.board[move.row][move.col] = '';
                return move;
            }
            this.gameState.board[move.row][move.col] = '';
        }
        return null;
    }
    
    getAvailableMoves() {
        return this.getAvailableMovesFromBoard(this.gameState.board);
    }
    
    getAvailableMovesFromBoard(board) {
        const moves = [];
        const size = this.gameSettings.boardSize;
        for (let row = 0; row < size; row++) {
            for (let col = 0; col < size; col++) {
                if (board[row][col] === '') {
                    moves.push({ row, col });
                }
            }
        }
        return moves;
    }
    
    // ===== GAME HELPERS =====
    showHint() {
        if (this.gameSettings.gameMode !== 'ai' || this.gameState.currentPlayer !== 'X') {
            this.showNotification('Gợi ý chỉ khả dụng khi chơi với máy và đến lượt bạn!', 'warning');
            return;
        }
        
        const move = this.getMediumAIMove();
        if (move) {
            const cell = document.querySelector(`[data-row="${move.row}"][data-col="${move.col}"]`);
            cell.classList.add('hint');
            setTimeout(() => cell.classList.remove('hint'), 3000);
            this.showNotification('Ô được đề xuất đã được highlight!', 'info');
        }
    }
    
    undoMove() {
        if (this.gameState.moveHistory.length === 0) {
            this.showNotification('Không có nước đi nào để hoàn tác!', 'warning');
            return;
        }
        
        // Undo one or two moves (if playing against AI)
        const movesToUndo = this.gameSettings.gameMode === 'ai' ? 
            Math.min(2, this.gameState.moveHistory.length) : 1;
        
        for (let i = 0; i < movesToUndo; i++) {
            const lastMove = this.gameState.moveHistory.pop();
            this.gameState.board[lastMove.row][lastMove.col] = '';
            
            const cell = document.querySelector(`[data-row="${lastMove.row}"][data-col="${lastMove.col}"]`);
            cell.textContent = '';
            cell.className = 'cell';
        }
        
        // Reset current player
        this.gameState.currentPlayer = this.gameState.moveHistory.length % 2 === 0 ? 'X' : 'O';
        this.gameState.isAITurn = false;
        this.updateDisplay();
    }
    
    checkWinner(row, col, player) {
        const size = this.gameSettings.boardSize;
        const winCondition = this.gameSettings.winCondition;
        const directions = [[0, 1], [1, 0], [1, 1], [1, -1]]; // horizontal, vertical, diagonal
        
        for (const [dr, dc] of directions) {
            let count = 1;
            const winningCells = [{ row, col }];
            
            // Check positive direction
            for (let i = 1; i < winCondition; i++) {
                const newRow = row + i * dr;
                const newCol = col + i * dc;
                if (newRow >= 0 && newRow < size && newCol >= 0 && newCol < size &&
                    this.gameState.board[newRow][newCol] === player) {
                    count++;
                    winningCells.push({ row: newRow, col: newCol });
                } else break;
            }
            
            // Check negative direction
            for (let i = 1; i < winCondition; i++) {
                const newRow = row - i * dr;
                const newCol = col - i * dc;
                if (newRow >= 0 && newRow < size && newCol >= 0 && newCol < size &&
                    this.gameState.board[newRow][newCol] === player) {
                    count++;
                    winningCells.push({ row: newRow, col: newCol });
                } else break;
            }
            
            if (count >= winCondition) {
                this.highlightWinningCells(winningCells);
                return true;
            }
        }
        
        return false;
    }
    
    checkDraw() {
        const size = this.gameSettings.boardSize;
        for (let row = 0; row < size; row++) {
            for (let col = 0; col < size; col++) {
                if (this.gameState.board[row][col] === '') {
                    return false;
                }
            }
        }
        return true;
    }
    
    // ===== UI UPDATES =====
    updateCellDisplay(row, col, player) {
        const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
        cell.textContent = player;
        cell.classList.add(player.toLowerCase());
        
        // Animation
        cell.style.transform = 'scale(0)';
        setTimeout(() => {
            cell.style.transform = 'scale(1)';
        }, 50);
    }
    
    highlightWinningCells(cells) {
        cells.forEach(({ row, col }) => {
            const cell = document.querySelector(`[data-row="${row}"][data-col="${col}"]`);
            cell.classList.add('winning');
        });
    }
    
    updateDisplay() {
        document.getElementById('current-player').textContent = this.gameState.currentPlayer;
        document.getElementById('current-player').style.color = 
            this.gameState.currentPlayer === 'X' ? 'var(--danger-color)' : 'var(--primary-color)';
    }
    
    updateScore() {
        document.getElementById('score-x').textContent = this.gameState.score.X;
        document.getElementById('score-o').textContent = this.gameState.score.O;
        
        // Animation
        const scoreElement = this.gameState.currentPlayer === 'X' ? 
            document.getElementById('score-x') : document.getElementById('score-o');
        scoreElement.style.transform = 'scale(1.3)';
        scoreElement.style.color = 'var(--success-color)';
        setTimeout(() => {
            scoreElement.style.transform = 'scale(1)';
            scoreElement.style.color = '';
        }, 300);
    }
    
    updateGameStatus(message) {
        document.getElementById('game-status').textContent = message;
    }
    
    switchPlayer() {
        this.gameState.currentPlayer = this.gameState.currentPlayer === 'X' ? 'O' : 'X';
        this.updateDisplay();
    }
    
    handleGameEnd(result, winner = null) {
        this.gameState.gameActive = false;
        
        let title, message;
        if (result === 'win') {
            this.gameState.score[winner]++;
            this.updateScore();
            
            if (this.gameSettings.gameMode === 'ai') {
                if (winner === 'X') {
                    title = '🎉 Bạn thắng!';
                    message = 'Chúc mừng! Bạn đã đánh bại máy tính!';
                } else {
                    title = '🤖 Máy thắng!';
                    message = 'Máy tính đã thắng! Hãy thử lại nhé!';
                }
            } else {
                title = `🎉 Người chơi ${winner} thắng!`;
                message = `Chúc mừng! Người chơi ${winner} đã giành chiến thắng!`;
            }
            this.updateGameStatus(title);
        } else {
            title = '🤝 Hòa!';
            message = 'Trận đấu kết thúc với kết quả hòa!';
            this.updateGameStatus(title);
        }
        
        this.showModal(title, message);
        this.disableAllCells();
    }
    
    disableAllCells() {
        document.querySelectorAll('.cell').forEach(cell => {
            cell.classList.add('disabled');
        });
    }
    
    resetGame() {
        this.initializeGame();
        this.showNotification('Game đã được reset!', 'success');
    }
    
    newGame() {
        this.resetGame();
        this.gameState.score = { X: 0, O: 0 };
        this.updateScore();
        this.showNotification('Bắt đầu game mới!', 'success');
    }
    
    // ===== MODAL & NOTIFICATIONS =====
    showModal(title, message) {
        document.getElementById('result-title').textContent = title;
        document.getElementById('result-message').textContent = message;
        document.getElementById('result-modal').style.display = 'block';
    }
    
    closeModal() {
        document.getElementById('result-modal').style.display = 'none';
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 10000;
            animation: slideInRight 0.3s ease;
            max-width: 300px;
            word-wrap: break-word;
        `;
        
        // Set background color based on type
        const colors = {
            success: '#50c878',
            warning: '#ffa500',
            info: '#17a2b8',
            error: '#ff6b6b'
        };
        notification.style.backgroundColor = colors[type] || colors.info;
        
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }
    
    // ===== KEYBOARD HANDLING =====
    handleKeyPress(event) {
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'SELECT') return;
        
        const key = event.key.toLowerCase();
        
        switch (key) {
            case 'escape':
                if (document.getElementById('result-modal').style.display === 'block') {
                    this.closeModal();
                } else if (!this.screens.menu.classList.contains('hidden')) {
                    // Already on menu
                } else {
                    this.showScreen('menu');
                }
                break;
            case 'r':
                if (!this.screens.game.classList.contains('hidden')) {
                    this.resetGame();
                }
                break;
            case 'n':
                if (!this.screens.game.classList.contains('hidden')) {
                    this.newGame();
                }
                break;
            case 'h':
                if (!this.screens.game.classList.contains('hidden')) {
                    this.showHint();
                }
                break;
            case 'u':
                if (!this.screens.game.classList.contains('hidden')) {
                    this.undoMove();
                }
                break;
        }
        
        // Number keys for 3x3 board
        if (this.gameSettings.boardSize === 3 && /[1-9]/.test(key)) {
            const index = parseInt(key) - 1;
            const row = Math.floor(index / 3);
            const col = index % 3;
            this.handleCellClick(row, col);
        }
    }
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize game when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AdvancedCaroGame();
});
