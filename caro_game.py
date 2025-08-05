import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import math

class AdvancedCaroGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game Cờ Caro - Advanced")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Game settings
        self.settings = {
            'board_size': 5,
            'win_condition': 5,
            'game_mode': 'human',  # 'human' or 'ai'
            'ai_difficulty': 'medium',  # 'easy', 'medium', 'hard'
            'theme': 'default'  # 'default', 'dark'
        }
        
        # Game state
        self.game_state = {
            'board': [],
            'current_player': 'X',
            'game_active': False,
            'score': {'X': 0, 'O': 0},
            'move_history': [],
            'is_ai_turn': False
        }
        
        # Load settings
        self.load_settings()
        
        # Setup colors and fonts
        self.setup_style()
        
        # Initialize screens
        self.current_screen = None
        self.show_menu()
    
    def setup_style(self):
        if self.settings['theme'] == 'dark':
            self.colors = {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'primary': '#4a90e2',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'light': '#3d3d3d',
                'button_bg': '#4a4a4a'
            }
        else:
            self.colors = {
                'bg': '#f0f2f5',
                'fg': '#2c3e50',
                'primary': '#4a90e2',
                'secondary': '#6c757d',
                'success': '#28a745',
                'danger': '#dc3545',
                'warning': '#ffc107',
                'info': '#17a2b8',
                'light': '#ffffff',
                'button_bg': '#ffffff'
            }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.fonts = {
            'title': ('Arial', 24, 'bold'),
            'heading': ('Arial', 16, 'bold'),
            'button': ('Arial', 12, 'bold'),
            'text': ('Arial', 10),
            'cell': ('Arial', 20, 'bold')
        }
    
    # ===== SCREEN MANAGEMENT =====
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_menu(self):
        self.clear_screen()
        self.current_screen = 'menu'
        
        # Title
        title = tk.Label(
            self.root, 
            text="🎮 GAME CỜ CARO 🎮",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title.pack(pady=50)
        
        # Menu buttons
        button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        button_frame.pack(pady=20)
        
        buttons = [
            ("👥 Chơi với người", lambda: self.start_game('human')),
            ("🤖 Chơi với máy", lambda: self.start_game('ai')),
            ("⚙️ Cài đặt", self.show_settings),
            ("ℹ️ Hướng dẫn", self.show_help),
            ("❌ Thoát", self.quit_game)
        ]
        
        for text, command in buttons:
            btn = tk.Button(
                button_frame,
                text=text,
                font=self.fonts['button'],
                bg=self.colors['primary'],
                fg='white',
                width=20,
                height=2,
                relief='raised',
                bd=2,
                cursor='hand2',
                command=command
            )
            btn.pack(pady=10)
    
    def show_settings(self):
        self.clear_screen()
        self.current_screen = 'settings'
        
        # Title
        title = tk.Label(
            self.root,
            text="⚙️ Cài đặt Game",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['fg']
        )
        title.pack(pady=30)
        
        # Settings frame
        settings_frame = tk.Frame(self.root, bg=self.colors['bg'])
        settings_frame.pack(pady=20, padx=50, fill='both', expand=True)
        
        # Board size
        tk.Label(settings_frame, text="Kích thước bàn cờ:", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 5))
        self.board_size_var = tk.StringVar(value=str(self.settings['board_size']))
        board_size_combo = ttk.Combobox(settings_frame, textvariable=self.board_size_var, values=['3', '4', '5', '6', '7', '8', '9', '10'], state='readonly', font=self.fonts['text'])
        board_size_combo.pack(fill='x', pady=(0, 15))
        board_size_combo.bind('<<ComboboxSelected>>', self.on_board_size_change)
        
        # Win condition
        tk.Label(settings_frame, text="Số quân cần để thắng:", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 5))
        self.win_condition_var = tk.StringVar(value=str(self.settings['win_condition']))
        self.win_condition_combo = ttk.Combobox(settings_frame, textvariable=self.win_condition_var, state='readonly', font=self.fonts['text'])
        self.win_condition_combo.pack(fill='x', pady=(0, 15))
        self.update_win_condition_options()
        
        # AI difficulty
        tk.Label(settings_frame, text="Độ khó AI:", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 5))
        self.ai_difficulty_var = tk.StringVar(value=self.settings['ai_difficulty'])
        ai_combo = ttk.Combobox(settings_frame, textvariable=self.ai_difficulty_var, values=['easy', 'medium', 'hard'], state='readonly', font=self.fonts['text'])
        ai_combo.pack(fill='x', pady=(0, 15))
        
        # Theme
        tk.Label(settings_frame, text="Giao diện:", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['fg']).pack(anchor='w', pady=(0, 5))
        self.theme_var = tk.StringVar(value=self.settings['theme'])
        theme_combo = ttk.Combobox(settings_frame, textvariable=self.theme_var, values=['default', 'dark'], state='readonly', font=self.fonts['text'])
        theme_combo.pack(fill='x', pady=(0, 15))
        
        # Buttons
        button_frame = tk.Frame(settings_frame, bg=self.colors['bg'])
        button_frame.pack(pady=30)
        
        save_btn = tk.Button(button_frame, text="💾 Lưu cài đặt", font=self.fonts['button'], bg=self.colors['success'], fg='white', command=self.save_settings)
        save_btn.pack(side='left', padx=10)
        
        back_btn = tk.Button(button_frame, text="🔙 Quay lại", font=self.fonts['button'], bg=self.colors['secondary'], fg='white', command=self.show_menu)
        back_btn.pack(side='right', padx=10)
    
    def on_board_size_change(self, event=None):
        self.update_win_condition_options()
    
    def update_win_condition_options(self):
        size = int(self.board_size_var.get())
        options = [str(i) for i in range(3, min(size + 1, 7))]
        self.win_condition_combo['values'] = options
        if self.win_condition_var.get() not in options:
            self.win_condition_var.set(str(min(5, size)))
    
    def save_settings(self):
        self.settings['board_size'] = int(self.board_size_var.get())
        self.settings['win_condition'] = int(self.win_condition_var.get())
        self.settings['ai_difficulty'] = self.ai_difficulty_var.get()
        old_theme = self.settings['theme']
        self.settings['theme'] = self.theme_var.get()
        
        self.save_settings_to_file()
        
        if old_theme != self.settings['theme']:
            self.setup_style()
            messagebox.showinfo("Cài đặt", "Cài đặt đã được lưu! Khởi động lại để áp dụng theme mới.")
        else:
            messagebox.showinfo("Cài đặt", "Cài đặt đã được lưu!")
    
    def show_help(self):
        help_text = """
🎯 MỤC TIÊU:
Đặt các quân cờ thành một hàng liên tiếp để thắng.

🎮 CÁCH CHƠI:
• Click vào ô trống để đặt quân
• Người chơi X luôn đi trước
• AI sẽ tự động đi sau bạn

⚙️ CÀI ĐẶT:
• Kích thước bàn: 3x3 đến 10x10
• Số quân thắng: 3-6 quân
• Độ khó AI: Dễ, Trung bình, Khó

⌨️ PHÍM TẮT:
• R: Chơi lại
• N: Game mới
• H: Gợi ý (chỉ với AI)
• U: Hoàn tác
• Q: Thoát

🤖 ĐỘ KHÓ AI:
• Dễ: Đi ngẫu nhiên
• Trung bình: Có chiến thuật
• Khó: Thuật toán thông minh
        """
        messagebox.showinfo("Hướng dẫn", help_text)
    
    # ===== GAME LOGIC =====
    def start_game(self, mode):
        self.settings['game_mode'] = mode
        self.initialize_game()
        self.show_game_screen()
    
    def initialize_game(self):
        size = self.settings['board_size']
        self.game_state['board'] = [['' for _ in range(size)] for _ in range(size)]
        self.game_state['current_player'] = 'X'
        self.game_state['game_active'] = True
        self.game_state['move_history'] = []
        self.game_state['is_ai_turn'] = False
    
    def show_game_screen(self):
        self.clear_screen()
        self.current_screen = 'game'
        
        # Header
        header_frame = tk.Frame(self.root, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=10, pady=5)
        
        back_btn = tk.Button(header_frame, text="🏠 Menu", font=self.fonts['button'], bg=self.colors['secondary'], fg='white', command=self.show_menu)
        back_btn.pack(side='left')
        
        title = tk.Label(header_frame, text="Game Cờ Caro", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['fg'])
        title.pack(side='left', padx=20)
        
        settings_btn = tk.Button(header_frame, text="⚙️", font=self.fonts['button'], bg=self.colors['info'], fg='white', command=self.show_settings)
        settings_btn.pack(side='right')
        
        # Game info
        info_frame = tk.Frame(self.root, bg=self.colors['light'], relief='raised', bd=2)
        info_frame.pack(fill='x', padx=10, pady=5)
        
        # Current player and mode
        player_frame = tk.Frame(info_frame, bg=self.colors['light'])
        player_frame.pack(pady=10)
        
        self.current_player_label = tk.Label(player_frame, text=f"Lượt của: {self.game_state['current_player']}", font=self.fonts['heading'], bg=self.colors['light'])
        self.current_player_label.pack()
        
        mode_text = "🤖 Chơi với máy" if self.settings['game_mode'] == 'ai' else "👥 Hai người chơi"
        tk.Label(player_frame, text=mode_text, font=self.fonts['text'], bg=self.colors['light']).pack()
        
        # Score
        score_frame = tk.Frame(info_frame, bg=self.colors['light'])
        score_frame.pack(pady=5)
        
        tk.Label(score_frame, text="ĐIỂM SỐ", font=self.fonts['button'], bg=self.colors['light']).pack()
        
        scores_container = tk.Frame(score_frame, bg=self.colors['light'])
        scores_container.pack()
        
        self.score_x_label = tk.Label(scores_container, text=f"X: {self.game_state['score']['X']}", font=self.fonts['text'], bg=self.colors['light'], fg=self.colors['danger'])
        self.score_x_label.pack(side='left', padx=20)
        
        player_o_name = "🤖 Máy" if self.settings['game_mode'] == 'ai' else "O"
        self.score_o_label = tk.Label(scores_container, text=f"{player_o_name}: {self.game_state['score']['O']}", font=self.fonts['text'], bg=self.colors['light'], fg=self.colors['primary'])
        self.score_o_label.pack(side='right', padx=20)
        
        # Game board
        self.create_game_board()
        
        # Game status
        self.status_label = tk.Label(self.root, text="", font=self.fonts['heading'], bg=self.colors['bg'], fg=self.colors['success'])
        self.status_label.pack(pady=10)
        
        # Control buttons
        control_frame = tk.Frame(self.root, bg=self.colors['bg'])
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(control_frame, text="🔄 Chơi lại", font=self.fonts['button'], bg=self.colors['warning'], fg='white', command=self.reset_game)
        reset_btn.pack(side='left', padx=5)
        
        new_btn = tk.Button(control_frame, text="🆕 Game mới", font=self.fonts['button'], bg=self.colors['success'], fg='white', command=self.new_game)
        new_btn.pack(side='left', padx=5)
        
        if self.settings['game_mode'] == 'ai':
            hint_btn = tk.Button(control_frame, text="💡 Gợi ý", font=self.fonts['button'], bg=self.colors['info'], fg='white', command=self.show_hint)
            hint_btn.pack(side='left', padx=5)
        
        undo_btn = tk.Button(control_frame, text="↶ Hoàn tác", font=self.fonts['button'], bg=self.colors['secondary'], fg='white', command=self.undo_move)
        undo_btn.pack(side='left', padx=5)
        
        # Keyboard bindings
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def create_game_board(self):
        board_frame = tk.Frame(self.root, bg=self.colors['bg'])
        board_frame.pack(pady=20)
        
        size = self.settings['board_size']
        self.board_buttons = []
        
        # Calculate button size based on board size
        button_size = max(2, 8 - size // 2)
        font_size = max(12, 24 - size * 2)
        
        for i in range(size):
            row = []
            for j in range(size):
                btn = tk.Button(
                    board_frame,
                    text='',
                    font=('Arial', font_size, 'bold'),
                    width=button_size,
                    height=button_size//2,
                    command=lambda r=i, c=j: self.make_move(r, c),
                    bg=self.colors['button_bg'],
                    relief='raised',
                    bd=2,
                    cursor='hand2'
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.board_buttons.append(row)
    
    def make_move(self, row, col):
        if (not self.game_state['game_active'] or 
            self.game_state['board'][row][col] != '' or 
            self.game_state['is_ai_turn']):
            return
        
        # Make move
        player = self.game_state['current_player']
        self.game_state['board'][row][col] = player
        self.game_state['move_history'].append((row, col, player))
        
        # Update UI
        btn = self.board_buttons[row][col]
        btn.config(text=player, state='disabled')
        if player == 'X':
            btn.config(fg=self.colors['danger'], bg='#ffe6e6')
        else:
            btn.config(fg=self.colors['primary'], bg='#e6f3ff')
        
        # Check win/draw
        if self.check_winner(row, col, player):
            self.handle_game_end('win', player)
            return
        
        if self.check_draw():
            self.handle_game_end('draw')
            return
        
        # Switch player
        self.switch_player()
        
        # AI move
        if self.settings['game_mode'] == 'ai' and self.game_state['current_player'] == 'O':
            self.game_state['is_ai_turn'] = True
            self.root.after(500, self.make_ai_move)
    
    def make_ai_move(self):
        if not self.game_state['game_active']:
            return
        
        move = None
        difficulty = self.settings['ai_difficulty']
        
        if difficulty == 'easy':
            move = self.get_random_move()
        elif difficulty == 'medium':
            move = self.get_medium_ai_move()
        else:  # hard
            move = self.get_hard_ai_move()
        
        if move:
            self.game_state['is_ai_turn'] = False
            self.make_move(move[0], move[1])
    
    # ===== AI ALGORITHMS =====
    def get_random_move(self):
        moves = self.get_available_moves()
        return random.choice(moves) if moves else None
    
    def get_medium_ai_move(self):
        # Check for winning move
        move = self.find_winning_move('O')
        if move:
            return move
        
        # Block player winning move
        move = self.find_winning_move('X')
        if move:
            return move
        
        # Take center if available
        size = self.settings['board_size']
        center = size // 2
        if self.game_state['board'][center][center] == '':
            return (center, center)
        
        # Random move
        return self.get_random_move()
    
    def get_hard_ai_move(self):
        # Simple minimax for smaller boards
        if self.settings['board_size'] <= 5:
            return self.minimax_move()
        else:
            return self.get_medium_ai_move()
    
    def minimax_move(self):
        best_score = -float('inf')
        best_move = None
        
        for row, col in self.get_available_moves():
            self.game_state['board'][row][col] = 'O'
            score = self.minimax(False, 3)
            self.game_state['board'][row][col] = ''
            
            if score > best_score:
                best_score = score
                best_move = (row, col)
        
        return best_move
    
    def minimax(self, is_maximizing, depth):
        if depth == 0:
            return self.evaluate_board()
        
        moves = self.get_available_moves()
        if not moves:
            return 0
        
        if is_maximizing:
            max_score = -float('inf')
            for row, col in moves:
                self.game_state['board'][row][col] = 'O'
                score = self.minimax(False, depth - 1)
                self.game_state['board'][row][col] = ''
                max_score = max(score, max_score)
            return max_score
        else:
            min_score = float('inf')
            for row, col in moves:
                self.game_state['board'][row][col] = 'X'
                score = self.minimax(True, depth - 1)
                self.game_state['board'][row][col] = ''
                min_score = min(score, min_score)
            return min_score
    
    def evaluate_board(self):
        # Simple evaluation function
        score = 0
        size = self.settings['board_size']
        
        # Check all directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for row in range(size):
            for col in range(size):
                for dr, dc in directions:
                    score += self.evaluate_line(row, col, dr, dc, 'O') * 10
                    score -= self.evaluate_line(row, col, dr, dc, 'X') * 10
        
        return score
    
    def evaluate_line(self, row, col, dr, dc, player):
        count = 0
        size = self.settings['board_size']
        win_condition = self.settings['win_condition']
        
        for i in range(win_condition):
            r, c = row + i * dr, col + i * dc
            if 0 <= r < size and 0 <= c < size and self.game_state['board'][r][c] == player:
                count += 1
            else:
                break
        
        return count
    
    def find_winning_move(self, player):
        for row, col in self.get_available_moves():
            self.game_state['board'][row][col] = player
            if self.check_winner(row, col, player):
                self.game_state['board'][row][col] = ''
                return (row, col)
            self.game_state['board'][row][col] = ''
        return None
    
    def get_available_moves(self):
        moves = []
        size = self.settings['board_size']
        for row in range(size):
            for col in range(size):
                if self.game_state['board'][row][col] == '':
                    moves.append((row, col))
        return moves
    
    # ===== GAME HELPERS =====
    def show_hint(self):
        if self.settings['game_mode'] != 'ai' or self.game_state['current_player'] != 'X':
            messagebox.showwarning("Gợi ý", "Gợi ý chỉ khả dụng khi chơi với máy và đến lượt bạn!")
            return
        
        move = self.get_medium_ai_move()
        if move:
            btn = self.board_buttons[move[0]][move[1]]
            original_bg = btn.cget('bg')
            btn.config(bg='yellow')
            self.root.after(2000, lambda: btn.config(bg=original_bg))
            messagebox.showinfo("Gợi ý", f"Đề xuất: Hàng {move[0]+1}, Cột {move[1]+1}")
    
    def undo_move(self):
        if not self.game_state['move_history']:
            messagebox.showwarning("Hoàn tác", "Không có nước đi nào để hoàn tác!")
            return
        
        # Undo moves (1 for human vs human, 2 for human vs AI)
        moves_to_undo = 2 if self.settings['game_mode'] == 'ai' else 1
        moves_to_undo = min(moves_to_undo, len(self.game_state['move_history']))
        
        for _ in range(moves_to_undo):
            if self.game_state['move_history']:
                row, col, player = self.game_state['move_history'].pop()
                self.game_state['board'][row][col] = ''
                btn = self.board_buttons[row][col]
                btn.config(text='', state='normal', bg=self.colors['button_bg'], fg='black')
        
        # Reset current player
        self.game_state['current_player'] = 'X' if len(self.game_state['move_history']) % 2 == 0 else 'O'
        self.game_state['is_ai_turn'] = False
        self.update_current_player_display()
    
    def check_winner(self, row, col, player):
        size = self.settings['board_size']
        win_condition = self.settings['win_condition']
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            count = 1
            winning_cells = [(row, col)]
            
            # Check positive direction
            for i in range(1, win_condition):
                new_row, new_col = row + i * dr, col + i * dc
                if (0 <= new_row < size and 0 <= new_col < size and 
                    self.game_state['board'][new_row][new_col] == player):
                    count += 1
                    winning_cells.append((new_row, new_col))
                else:
                    break
            
            # Check negative direction
            for i in range(1, win_condition):
                new_row, new_col = row - i * dr, col - i * dc
                if (0 <= new_row < size and 0 <= new_col < size and 
                    self.game_state['board'][new_row][new_col] == player):
                    count += 1
                    winning_cells.append((new_row, new_col))
                else:
                    break
            
            if count >= win_condition:
                self.highlight_winning_cells(winning_cells)
                return True
        
        return False
    
    def highlight_winning_cells(self, cells):
        for row, col in cells:
            self.board_buttons[row][col].config(bg='lightgreen')
    
    def check_draw(self):
        size = self.settings['board_size']
        for row in range(size):
            for col in range(size):
                if self.game_state['board'][row][col] == '':
                    return False
        return True
    
    def switch_player(self):
        self.game_state['current_player'] = 'O' if self.game_state['current_player'] == 'X' else 'X'
        self.update_current_player_display()
    
    def update_current_player_display(self):
        player = self.game_state['current_player']
        self.current_player_label.config(text=f"Lượt của: {player}")
        if player == 'X':
            self.current_player_label.config(fg=self.colors['danger'])
        else:
            self.current_player_label.config(fg=self.colors['primary'])
    
    def handle_game_end(self, result, winner=None):
        self.game_state['game_active'] = False
        
        if result == 'win':
            self.game_state['score'][winner] += 1
            self.update_score_display()
            
            if self.settings['game_mode'] == 'ai':
                if winner == 'X':
                    title = "🎉 Bạn thắng!"
                    message = "Chúc mừng! Bạn đã đánh bại máy tính!"
                else:
                    title = "🤖 Máy thắng!"
                    message = "Máy tính đã thắng! Hãy thử lại nhé!"
            else:
                title = f"🎉 Người chơi {winner} thắng!"
                message = f"Chúc mừng! Người chơi {winner} đã giành chiến thắng!"
            
            self.status_label.config(text=title)
            messagebox.showinfo("Kết quả", message)
        else:
            title = "🤝 Hòa!"
            message = "Trận đấu kết thúc với kết quả hòa!"
            self.status_label.config(text=title)
            messagebox.showinfo("Kết quả", message)
        
        self.disable_all_buttons()
    
    def disable_all_buttons(self):
        size = self.settings['board_size']
        for row in range(size):
            for col in range(size):
                self.board_buttons[row][col].config(state='disabled')
    
    def update_score_display(self):
        self.score_x_label.config(text=f"X: {self.game_state['score']['X']}")
        player_o_name = "🤖 Máy" if self.settings['game_mode'] == 'ai' else "O"
        self.score_o_label.config(text=f"{player_o_name}: {self.game_state['score']['O']}")
    
    def reset_game(self):
        self.initialize_game()
        if self.current_screen == 'game':
            self.show_game_screen()
        messagebox.showinfo("Reset", "Game đã được reset!")
    
    def new_game(self):
        self.game_state['score'] = {'X': 0, 'O': 0}
        self.reset_game()
        messagebox.showinfo("Game mới", "Bắt đầu game mới!")
    
    # ===== SETTINGS =====
    def load_settings(self):
        try:
            if os.path.exists('caro_settings.json'):
                with open('caro_settings.json', 'r') as f:
                    saved_settings = json.load(f)
                    self.settings.update(saved_settings)
        except:
            pass
    
    def save_settings_to_file(self):
        try:
            with open('caro_settings.json', 'w') as f:
                json.dump(self.settings, f)
        except:
            pass
    
    # ===== KEYBOARD HANDLING =====
    def on_key_press(self, event):
        key = event.char.lower()
        
        if key == 'r' and self.current_screen == 'game':
            self.reset_game()
        elif key == 'n' and self.current_screen == 'game':
            self.new_game()
        elif key == 'h' and self.current_screen == 'game':
            self.show_hint()
        elif key == 'u' and self.current_screen == 'game':
            self.undo_move()
        elif key == 'q':
            self.quit_game()
        
        # Number keys for small boards
        if (self.current_screen == 'game' and 
            self.settings['board_size'] == 3 and 
            event.char.isdigit() and 1 <= int(event.char) <= 9):
            index = int(event.char) - 1
            row, col = index // 3, index % 3
            self.make_move(row, col)
    
    def quit_game(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát game?"):
            self.save_settings_to_file()
            self.root.quit()
    
    def run(self):
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)
        self.root.mainloop()

if __name__ == "__main__":
    game = AdvancedCaroGame()
    game.run()
