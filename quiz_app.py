import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import cv2
import mediapipe as mp
import numpy as np
import threading

class QuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Quiz System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e3a8a')  # Dark blue background
        
        # Color scheme
        self.colors = {
            'bg_primary': '#1e3a8a',      # Dark blue
            'bg_secondary': '#1e40af',     # Slightly lighter blue
            'text_primary': '#ffffff',     # White
            'text_secondary': '#e5e7eb',   # Light gray
            'button_primary': '#0ea5e9',   # Sky blue
            'button_text': '#000000',      # Black
            'accent': '#10b981',           # Green
            'warning': '#f59e0b',          # Orange
            'error': '#ef4444'             # Red
        }
        
        # Data storage
        self.questions_file = "questions.json"
        self.questions = self.load_questions()
        
        # Current user type
        self.current_mode = None
        
        # Initialize main menu
        self.create_main_menu()
        
    def load_questions(self):
        if os.path.exists(self.questions_file):
            with open(self.questions_file, 'r') as f:
                return json.load(f)
        return {"multiple_choice": [], "true_false": [], "matching": []}
    
    def save_questions(self):
        with open(self.questions_file, 'w') as f:
            json.dump(self.questions, f, indent=2)
    
    def create_main_menu(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main container
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title with gradient effect
        title_frame = tk.Frame(main_container, bg=self.colors['bg_primary'], height=150)
        title_frame.pack(fill=tk.X, pady=50)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎯 Hand Gesture Quiz System", 
                              font=("Helvetica", 32, "bold"), 
                              bg=self.colors['bg_primary'], 
                              fg=self.colors['text_primary'])
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Interactive Learning with Hand Recognition", 
                                 font=("Helvetica", 14), 
                                 bg=self.colors['bg_primary'], 
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Buttons frame with better spacing
        buttons_frame = tk.Frame(main_container, bg=self.colors['bg_primary'])
        buttons_frame.pack(expand=True)
        
        # Teacher button with icon
        teacher_btn = tk.Button(buttons_frame, text="👨‍🏫 Teacher Mode", 
                               font=("Helvetica", 18, "bold"), 
                               bg=self.colors['button_primary'], 
                               fg=self.colors['button_text'],
                               width=20, height=2, 
                               relief=tk.RAISED, bd=3,
                               command=self.open_teacher_page,
                               cursor="hand2")
        teacher_btn.pack(pady=15)
        
        # Student button with icon
        student_btn = tk.Button(buttons_frame, text="🎓 Student Mode", 
                               font=("Helvetica", 18, "bold"), 
                               bg=self.colors['button_primary'], 
                               fg=self.colors['button_text'],
                               width=20, height=2, 
                               relief=tk.RAISED, bd=3,
                               command=self.open_student_page,
                               cursor="hand2")
        student_btn.pack(pady=15)
        
        # Exit button
        exit_btn = tk.Button(buttons_frame, text="❌ Exit", 
                            font=("Helvetica", 14, "bold"), 
                            bg=self.colors['error'], 
                            fg=self.colors['text_primary'],
                            width=15, height=1, 
                            relief=tk.RAISED, bd=2,
                            command=self.root.quit,
                            cursor="hand2")
        exit_btn.pack(pady=30)
    
    def open_teacher_page(self):
        self.current_mode = "teacher"
        self.create_teacher_interface()
    
    def open_student_page(self):
        self.current_mode = "student"
        self.create_student_interface()
    
    def create_teacher_interface(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        back_btn = tk.Button(header_frame, text="← Back to Menu", 
                            command=self.create_main_menu, 
                            bg=self.colors['button_primary'], 
                            fg=self.colors['button_text'],
                            font=("Helvetica", 12, "bold"),
                            cursor="hand2")
        back_btn.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text="👨‍🏫 Teacher Dashboard", 
                              font=("Helvetica", 24, "bold"), 
                              bg=self.colors['bg_primary'], 
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # Configure notebook style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.colors['bg_primary'])
        style.configure('TNotebook.Tab', background=self.colors['bg_secondary'], 
                       foreground=self.colors['text_primary'], padding=[20, 10])
        style.configure('TFrame', background=self.colors['bg_primary'])
        
        # Notebook for different question types
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Multiple Choice Tab
        self.create_multiple_choice_tab(notebook)
        
        # True/False Tab
        self.create_true_false_tab(notebook)
        
        # Matching Tab
        self.create_matching_tab(notebook)
        
        # View All Questions Tab
        self.create_view_questions_tab(notebook)
    
    def create_multiple_choice_tab(self, notebook):
        mc_frame = ttk.Frame(notebook)
        notebook.add(mc_frame, text="📝 Multiple Choice")
        mc_frame.configure(style='TFrame')
        
        # Question input
        tk.Label(mc_frame, text="Question:", font=("Helvetica", 14, "bold"),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10, 5))
        self.mc_question_entry = tk.Text(mc_frame, height=3, width=60, font=("Helvetica", 12),
                                        bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        self.mc_question_entry.pack(pady=(0, 10))
        
        # Options frame
        options_frame = tk.Frame(mc_frame, bg=self.colors['bg_primary'])
        options_frame.pack(pady=10)
        
        # Options with better styling
        for i, letter in enumerate(['A', 'B', 'C', 'D']):
            row = i
            tk.Label(options_frame, text=f"Option {letter}:", font=("Helvetica", 12, "bold"),
                    bg=self.colors['bg_primary'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky=tk.W, pady=8, padx=5)
            
            entry = tk.Entry(options_frame, width=40, font=("Helvetica", 11),
                           bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
            entry.grid(row=row, column=1, padx=10, pady=5)
            setattr(self, f'mc_option_{letter.lower()}', entry)
            
            var = tk.BooleanVar()
            setattr(self, f'mc_correct_{letter.lower()}', var)
            tk.Checkbutton(options_frame, text="✓ Correct", variable=var,
                          bg=self.colors['bg_primary'], fg=self.colors['accent'],
                          font=("Helvetica", 10, "bold")).grid(row=row, column=2, padx=10)
        
        # Add question button
        add_btn = tk.Button(mc_frame, text="➕ Add Question", command=self.add_multiple_choice,
                           bg=self.colors['accent'], fg=self.colors['text_primary'], 
                           font=("Helvetica", 14, "bold"), cursor="hand2",
                           relief=tk.RAISED, bd=3)
        add_btn.pack(pady=20)
    
    def create_true_false_tab(self, notebook):
        tf_frame = ttk.Frame(notebook)
        notebook.add(tf_frame, text="✅ True/False")
        tf_frame.configure(style='TFrame')
        
        # Question input
        tk.Label(tf_frame, text="Question:", font=("Helvetica", 14, "bold"),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10, 5))
        self.tf_question_entry = tk.Text(tf_frame, height=3, width=60, font=("Helvetica", 12),
                                        bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
        self.tf_question_entry.pack(pady=(0, 10))
        
        # Answer selection
        answer_frame = tk.Frame(tf_frame, bg=self.colors['bg_primary'])
        answer_frame.pack(pady=20)
        
        tk.Label(answer_frame, text="Correct Answer:", font=("Helvetica", 14, "bold"),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(side=tk.LEFT)
        self.tf_answer = tk.StringVar(value="True")
        tk.Radiobutton(answer_frame, text="✅ True", variable=self.tf_answer, value="True",
                      bg=self.colors['bg_primary'], fg=self.colors['accent'],
                      font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=15)
        tk.Radiobutton(answer_frame, text="❌ False", variable=self.tf_answer, value="False",
                      bg=self.colors['bg_primary'], fg=self.colors['error'],
                      font=("Helvetica", 12, "bold")).pack(side=tk.LEFT, padx=15)
        
        # Add question button
        add_btn = tk.Button(tf_frame, text="➕ Add Question", command=self.add_true_false,
                           bg=self.colors['accent'], fg=self.colors['text_primary'], 
                           font=("Helvetica", 14, "bold"), cursor="hand2",
                           relief=tk.RAISED, bd=3)
        add_btn.pack(pady=20)
    
    def create_matching_tab(self, notebook):
        match_frame = ttk.Frame(notebook)
        notebook.add(match_frame, text="🔗 Matching")
        match_frame.configure(style='TFrame')
        
        # Instructions
        tk.Label(match_frame, text="Create matching pairs:", font=("Helvetica", 14, "bold"),
                bg=self.colors['bg_primary'], fg=self.colors['text_primary']).pack(anchor=tk.W, pady=(10, 5))
        
        # Pairs frame
        pairs_frame = tk.Frame(match_frame, bg=self.colors['bg_primary'])
        pairs_frame.pack(pady=10)
        
        self.match_pairs = []
        
        # Add initial pair inputs
        for i in range(4):
            pair_frame = tk.Frame(pairs_frame, bg=self.colors['bg_primary'])
            pair_frame.pack(pady=8)
            
            tk.Label(pair_frame, text=f"Pair {i+1}:", font=("Helvetica", 12, "bold"),
                    bg=self.colors['bg_primary'], fg=self.colors['text_primary']).grid(row=0, column=0, sticky=tk.W)
            left_entry = tk.Entry(pair_frame, width=25, font=("Helvetica", 11),
                                 bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
            left_entry.grid(row=0, column=1, padx=5)
            tk.Label(pair_frame, text="matches with", font=("Helvetica", 10),
                    bg=self.colors['bg_primary'], fg=self.colors['text_secondary']).grid(row=0, column=2, padx=5)
            right_entry = tk.Entry(pair_frame, width=25, font=("Helvetica", 11),
                                  bg=self.colors['bg_secondary'], fg=self.colors['text_primary'])
            right_entry.grid(row=0, column=3, padx=5)
            
            self.match_pairs.append((left_entry, right_entry))
        
        # Add question button
        add_btn = tk.Button(match_frame, text="➕ Add Matching Question", command=self.add_matching,
                           bg=self.colors['accent'], fg=self.colors['text_primary'], 
                           font=("Helvetica", 14, "bold"), cursor="hand2",
                           relief=tk.RAISED, bd=3)
        add_btn.pack(pady=20)
    
    def create_view_questions_tab(self, notebook):
        view_frame = ttk.Frame(notebook)
        notebook.add(view_frame, text="👁️ View Questions")
        view_frame.configure(style='TFrame')
        
        # Questions display
        self.questions_text = scrolledtext.ScrolledText(view_frame, height=25, width=80,
                                                       font=("Consolas", 11),
                                                       bg=self.colors['bg_secondary'], 
                                                       fg=self.colors['text_primary'])
        self.questions_text.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Refresh button
        refresh_btn = tk.Button(view_frame, text="🔄 Refresh", command=self.refresh_questions_view,
                               bg=self.colors['button_primary'], fg=self.colors['button_text'],
                               font=("Helvetica", 12, "bold"), cursor="hand2")
        refresh_btn.pack(pady=10)
        
        # Initial load
        self.refresh_questions_view()
    
    def add_multiple_choice(self):
        question = self.mc_question_entry.get("1.0", tk.END).strip()
        options = {
            'A': self.mc_option_a.get(),
            'B': self.mc_option_b.get(),
            'C': self.mc_option_c.get(),
            'D': self.mc_option_d.get()
        }
        
        correct_answers = []
        if self.mc_correct_a.get(): correct_answers.append('A')
        if self.mc_correct_b.get(): correct_answers.append('B')
        if self.mc_correct_c.get(): correct_answers.append('C')
        if self.mc_correct_d.get(): correct_answers.append('D')
        
        if not question or not any(options.values()) or not correct_answers:
            messagebox.showerror("Error", "Please fill all fields and select at least one correct answer")
            return
        
        new_question = {
            'question': question,
            'options': options,
            'correct_answers': correct_answers
        }
        
        self.questions['multiple_choice'].append(new_question)
        self.save_questions()
        
        # Clear form
        self.mc_question_entry.delete("1.0", tk.END)
        self.mc_option_a.delete(0, tk.END)
        self.mc_option_b.delete(0, tk.END)
        self.mc_option_c.delete(0, tk.END)
        self.mc_option_d.delete(0, tk.END)
        self.mc_correct_a.set(False)
        self.mc_correct_b.set(False)
        self.mc_correct_c.set(False)
        self.mc_correct_d.set(False)
        
        messagebox.showinfo("Success", "Multiple choice question added successfully!")
    
    def add_true_false(self):
        question = self.tf_question_entry.get("1.0", tk.END).strip()
        answer = self.tf_answer.get()
        
        if not question:
            messagebox.showerror("Error", "Please enter a question")
            return
        
        new_question = {
            'question': question,
            'correct_answer': answer
        }
        
        self.questions['true_false'].append(new_question)
        self.save_questions()
        
        # Clear form
        self.tf_question_entry.delete("1.0", tk.END)
        self.tf_answer.set("True")
        
        messagebox.showinfo("Success", "True/False question added successfully!")
    
    def add_matching(self):
        pairs = []
        for left_entry, right_entry in self.match_pairs:
            left = left_entry.get().strip()
            right = right_entry.get().strip()
            if left and right:
                pairs.append({'left': left, 'right': right})
        
        if len(pairs) < 2:
            messagebox.showerror("Error", "Please enter at least 2 matching pairs")
            return
        
        new_question = {
            'pairs': pairs
        }
        
        self.questions['matching'].append(new_question)
        self.save_questions()
        
        # Clear form
        for left_entry, right_entry in self.match_pairs:
            left_entry.delete(0, tk.END)
            right_entry.delete(0, tk.END)
        
        messagebox.showinfo("Success", "Matching question added successfully!")
    
    def refresh_questions_view(self):
        self.questions_text.delete("1.0", tk.END)
        
        # Display Multiple Choice Questions
        self.questions_text.insert(tk.END, "🎯 MULTIPLE CHOICE QUESTIONS\n" + "="*50 + "\n\n")
        for i, q in enumerate(self.questions['multiple_choice'], 1):
            self.questions_text.insert(tk.END, f"Q{i}: {q['question']}\n")
            for key, value in q['options'].items():
                mark = " ✓" if key in q['correct_answers'] else ""
                self.questions_text.insert(tk.END, f"   {key}) {value}{mark}\n")
            self.questions_text.insert(tk.END, "\n")
        
        # Display True/False Questions
        self.questions_text.insert(tk.END, "\n✅ TRUE/FALSE QUESTIONS\n" + "="*50 + "\n\n")
        for i, q in enumerate(self.questions['true_false'], 1):
            self.questions_text.insert(tk.END, f"Q{i}: {q['question']}\n")
            self.questions_text.insert(tk.END, f"   Answer: {q['correct_answer']}\n\n")
        
        # Display Matching Questions
        self.questions_text.insert(tk.END, "\n🔗 MATCHING QUESTIONS\n" + "="*50 + "\n\n")
        for i, q in enumerate(self.questions['matching'], 1):
            self.questions_text.insert(tk.END, f"Matching Set {i}:\n")
            for j, pair in enumerate(q['pairs'], 1):
                self.questions_text.insert(tk.END, f"   {j}. {pair['left']} → {pair['right']}\n")
            self.questions_text.insert(tk.END, "\n")
    
    def create_student_interface(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        main_frame = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Header with gradient effect
        header_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        back_btn = tk.Button(header_frame, text="← Back to Menu", 
                            command=self.create_main_menu, 
                            bg=self.colors['button_primary'], 
                            fg=self.colors['button_text'],
                            font=("Helvetica", 12, "bold"),
                            cursor="hand2", relief=tk.RAISED, bd=2)
        back_btn.pack(side=tk.LEFT)
        
        title_label = tk.Label(header_frame, text="🎓 Student Dashboard", 
                              font=("Helvetica", 28, "bold"), 
                              bg=self.colors['bg_primary'], 
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=(30, 0))
        
        # Welcome message
        welcome_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'], relief=tk.RAISED, bd=2)
        welcome_frame.pack(fill=tk.X, pady=(0, 30), padx=20)
        
        welcome_label = tk.Label(welcome_frame, 
                                text="🚀 Welcome to Interactive Learning! Use your hands to answer questions!", 
                                font=("Helvetica", 16), 
                                bg=self.colors['bg_secondary'], 
                                fg=self.colors['text_primary'],
                                wraplength=800)
        welcome_label.pack(pady=15)
        
        # Quiz options with better design
        options_frame = tk.Frame(main_frame, bg=self.colors['bg_primary'])
        options_frame.pack(expand=True)
        
        # Hand Gesture Quiz - Enhanced
        gesture_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'], 
                                relief=tk.RAISED, bd=3, padx=20, pady=15)
        gesture_frame.pack(pady=20, fill=tk.X)
        
        gesture_title = tk.Label(gesture_frame, text="🤚 Hand Gesture Quiz", 
                                font=("Helvetica", 20, "bold"), 
                                bg=self.colors['bg_secondary'], 
                                fg=self.colors['text_primary'])
        gesture_title.pack()
        
        gesture_desc = tk.Label(gesture_frame, 
                               text="Answer questions by moving your hand to touch the correct answer!", 
                               font=("Helvetica", 12), 
                               bg=self.colors['bg_secondary'], 
                               fg=self.colors['text_secondary'])
        gesture_desc.pack(pady=5)
        
        gesture_btn = tk.Button(gesture_frame, text="🎯 Start Hand Gesture Quiz", 
                               font=("Helvetica", 16, "bold"), 
                               bg=self.colors['accent'], 
                               fg=self.colors['text_primary'],
                               width=25, height=2, 
                               command=self.start_hand_gesture_quiz,
                               cursor="hand2", relief=tk.RAISED, bd=3)
        gesture_btn.pack(pady=10)
        
        # Regular Quiz
        regular_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'], 
                                relief=tk.RAISED, bd=3, padx=20, pady=15)
        regular_frame.pack(pady=20, fill=tk.X)
        
        regular_title = tk.Label(regular_frame, text="📝 Regular Quiz", 
                                font=("Helvetica", 20, "bold"), 
                                bg=self.colors['bg_secondary'], 
                                fg=self.colors['text_primary'])
        regular_title.pack()
        
        regular_desc = tk.Label(regular_frame, 
                               text="Traditional quiz with mouse and keyboard interaction", 
                               font=("Helvetica", 12), 
                               bg=self.colors['bg_secondary'], 
                               fg=self.colors['text_secondary'])
        regular_desc.pack(pady=5)
        
        regular_btn = tk.Button(regular_frame, text="📋 Start Regular Quiz", 
                               font=("Helvetica", 16, "bold"), 
                               bg=self.colors['button_primary'], 
                               fg=self.colors['button_text'],
                               width=25, height=2, 
                               command=self.start_regular_quiz,
                               cursor="hand2", relief=tk.RAISED, bd=3)
        regular_btn.pack(pady=10)
        
        # View Scores
        scores_frame = tk.Frame(options_frame, bg=self.colors['bg_secondary'], 
                               relief=tk.RAISED, bd=3, padx=20, pady=15)
        scores_frame.pack(pady=20, fill=tk.X)
        
        scores_title = tk.Label(scores_frame, text="📊 View Scores", 
                               font=("Helvetica", 20, "bold"), 
                               bg=self.colors['bg_secondary'], 
                               fg=self.colors['text_primary'])
        scores_title.pack()
        
        scores_desc = tk.Label(scores_frame, 
                              text="Check your quiz performance and progress", 
                              font=("Helvetica", 12), 
                              bg=self.colors['bg_secondary'], 
                              fg=self.colors['text_secondary'])
        scores_desc.pack(pady=5)
        
        scores_btn = tk.Button(scores_frame, text="📈 View My Scores", 
                              font=("Helvetica", 16, "bold"), 
                              bg=self.colors['warning'], 
                              fg=self.colors['text_primary'],
                              width=25, height=2, 
                              command=self.view_scores,
                              cursor="hand2", relief=tk.RAISED, bd=3)
        scores_btn.pack(pady=10)
    
    def start_hand_gesture_quiz(self):
        # Check if there are any questions
        total_questions = len(self.questions['multiple_choice']) + len(self.questions['true_false'])
        if total_questions == 0:
            messagebox.showwarning("No Questions", "No questions available. Please ask your teacher to add questions.")
            return
        
        # Run the enhanced hand gesture quiz
        self.run_enhanced_hand_gesture_quiz()

    def start_regular_quiz(self):
        messagebox.showinfo("Coming Soon", "Regular quiz feature will be implemented soon!")
    
    def view_scores(self):
        messagebox.showinfo("Coming Soon", "Score viewing feature will be implemented soon!")
    
    def run_enhanced_hand_gesture_quiz(self):
        try:
            # Test camera first
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Camera Error", "Could not open camera")
                return
            
            # For macOS compatibility, create window before loop
            cv2.namedWindow('🎯 Hand Gesture Quiz - Interactive Learning', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('🎯 Hand Gesture Quiz - Interactive Learning', 1200, 800)
            
            # Initialize MediaPipe
            mp_hands = mp.solutions.hands
            mp_drawing = mp.solutions.drawing_utils
            hands = mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            )
            
            # Enhanced ball properties
            ball_pos = [600, 400]
            ball_radius = 25
            ball_color = (0, 255, 255)  # Cyan
            ball_trail = []
            
            # Quiz state
            current_question_index = 0
            quiz_answered = False
            answer_text = ""
            answer_timer = 0
            score = 0
            
            # Combine multiple choice and true/false questions
            all_questions = []
            
            # Add multiple choice questions
            for q in self.questions['multiple_choice']:
                all_questions.append({
                    'type': 'multiple_choice',
                    'question': q['question'],
                    'options': q['options'],
                    'correct_answers': q['correct_answers']
                })
            
            # Add true/false questions
            for q in self.questions['true_false']:
                all_questions.append({
                    'type': 'true_false',
                    'question': q['question'],
                    'correct_answer': q['correct_answer']
                })
            
            if not all_questions:
                messagebox.showwarning("No Questions", "No questions available for hand gesture quiz.")
                cap.release()
                return
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]
                
                # Create a beautiful gradient background
                overlay = np.zeros_like(frame)
                overlay[:] = (20, 40, 80)  # Dark blue
                frame = cv2.addWeighted(frame, 0.3, overlay, 0.7, 0)
                
                # Convert BGR to RGB for MediaPipe
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(rgb_frame)
                
                # Process hand landmarks
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Draw hand landmarks with style
                        mp_drawing.draw_landmarks(
                            frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=3, circle_radius=3),
                            mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=3)
                        )
                        
                        # Get index finger tip coordinates
                        index_finger_tip = hand_landmarks.landmark[8]
                        finger_x = int(index_finger_tip.x * width)
                        finger_y = int(index_finger_tip.y * height)
                        
                        # Update ball position with smoothing
                        ball_pos[0] = int(0.7 * ball_pos[0] + 0.3 * finger_x)
                        ball_pos[1] = int(0.7 * ball_pos[1] + 0.3 * finger_y)
                        
                        # Keep ball within boundaries
                        ball_pos[0] = max(ball_radius, min(width - ball_radius, ball_pos[0]))
                        ball_pos[1] = max(ball_radius, min(height - ball_radius, ball_pos[1]))
                        
                        # Add to trail
                        ball_trail.append(tuple(ball_pos))
                        if len(ball_trail) > 10:
                            ball_trail.pop(0)
                        
                        # Draw finger pointer
                        cv2.circle(frame, (finger_x, finger_y), 12, (255, 255, 0), -1)
                        cv2.circle(frame, (finger_x, finger_y), 12, (0, 0, 0), 2)
                
                # Draw ball trail
                for i, pos in enumerate(ball_trail):
                    alpha = i / len(ball_trail)
                    cv2.circle(frame, pos, int(ball_radius * alpha * 0.5), 
                              (int(ball_color[0] * alpha), int(ball_color[1] * alpha), int(ball_color[2] * alpha)), -1)
                
                # Draw main ball with glow effect
                cv2.circle(frame, tuple(ball_pos), ball_radius + 5, (100, 200, 255), 2)
                cv2.circle(frame, tuple(ball_pos), ball_radius, ball_color, -1)
                cv2.circle(frame, tuple(ball_pos), ball_radius, (255, 255, 255), 2)
                
                # Display current question
                if current_question_index < len(all_questions):
                    current_q = all_questions[current_question_index]
                    
                    # Draw question background
                    question_bg = np.zeros((120, width, 3), dtype=np.uint8)
                    question_bg[:] = (40, 60, 120)  # Blue background
                    frame[0:120, 0:width] = cv2.addWeighted(frame[0:120, 0:width], 0.3, question_bg, 0.7, 0)
                    
                    # Draw question text with better formatting
                    question_text = f"Question {current_question_index + 1}/{len(all_questions)}"
                    cv2.putText(frame, question_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                    
                    # Split long questions
                    question = current_q['question']
                    if len(question) > 60:
                        question = question[:60] + "..."
                    cv2.putText(frame, question, (20, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)
                    
                    # Draw answer boxes based on question type
                    answer_boxes = []
                    
                    if current_q['type'] == 'multiple_choice':
                        y_start = 150
                        for i, (key, option) in enumerate(current_q['options'].items()):
                            if option:  # Only show non-empty options
                                box = [20, y_start + i*80, 500, y_start + i*80 + 60]
                                answer_boxes.append((key, box, option))
                                
                                # Draw enhanced answer box
                                cv2.rectangle(frame, (box[0]-5, box[1]-5), (box[2]+5, box[3]+5), (0, 255, 0), 3)
                                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 150, 0), -1)
                                cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (255, 255, 255), 2)
                                
                                # Option text
                                cv2.putText(frame, f"{key})", (box[0] + 15, box[1] + 25), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                                cv2.putText(frame, option[:35], (box[0] + 50, box[1] + 40), 
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    elif current_q['type'] == 'true_false':
                        # True button
                        true_box = [50, 200, 300, 280]
                        answer_boxes.append(("True", true_box, "True"))
                        cv2.rectangle(frame, (true_box[0]-5, true_box[1]-5), (true_box[2]+5, true_box[3]+5), (0, 255, 0), 3)
                        cv2.rectangle(frame, (true_box[0], true_box[1]), (true_box[2], true_box[3]), (0, 200, 0), -1)
                        cv2.putText(frame, "✓ TRUE", (true_box[0] + 60, true_box[1] + 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
                        
                        # False button
                        false_box = [350, 200, 600, 280]
                        answer_boxes.append(("False", false_box, "False"))
                        cv2.rectangle(frame, (false_box[0]-5, false_box[1]-5), (false_box[2]+5, false_box[3]+5), (0, 0, 255), 3)
                        cv2.rectangle(frame, (false_box[0], false_box[1]), (false_box[2], false_box[3]), (0, 0, 200), -1)
                        cv2.putText(frame, "✗ FALSE", (false_box[0] + 50, false_box[1] + 50), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
                    
                    # Check collisions
                    if not quiz_answered:
                        for key, box, option in answer_boxes:
                            if (box[0] <= ball_pos[0] <= box[2] and box[1] <= ball_pos[1] <= box[3]):
                                quiz_answered = True
                                
                                if current_q['type'] == 'multiple_choice':
                                    if key in current_q['correct_answers']:
                                        answer_text = "🎉 CORRECT! Well Done!"
                                        score += 1
                                    else:
                                        correct_ans = ', '.join(current_q['correct_answers'])
                                        answer_text = f"❌ Wrong! Correct: {correct_ans}"
                                elif current_q['type'] == 'true_false':
                                    if key == current_q['correct_answer']:
                                        answer_text = "🎉 CORRECT! Excellent!"
                                        score += 1
                                    else:
                                        answer_text = f"❌ Wrong! Correct: {current_q['correct_answer']}"
                                
                                answer_timer = 180  # 3 seconds at 60fps
                
                # Display result with animation
                if quiz_answered and answer_timer > 0:
                    # Create result background
                    result_bg = np.zeros((150, width, 3), dtype=np.uint8)
                    if "CORRECT" in answer_text:
                        result_bg[:] = (0, 150, 0)  # Green
                        text_color = (255, 255, 255)
                    else:
                        result_bg[:] = (0, 0, 150)  # Red
                        text_color = (255, 255, 255)
                    
                    # Add pulsing effect
                    alpha = 0.8 + 0.2 * np.sin(answer_timer * 0.3)
                    y_pos = height//2 - 75
                    frame[y_pos:y_pos+150, 0:width] = cv2.addWeighted(
                        frame[y_pos:y_pos+150, 0:width], 1-alpha, result_bg, alpha, 0)
                    
                    # Display result text
                    cv2.putText(frame, answer_text, (width//2 - 200, height//2), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.2, text_color, 3)
                    answer_timer -= 1
                    
                    if answer_timer <= 0:
                        quiz_answered = False
                        current_question_index += 1
                        ball_trail.clear()
                        
                        # Check if quiz is complete
                        if current_question_index >= len(all_questions):
                            # Final score display
                            final_bg = np.zeros_like(frame)
                            final_bg[:] = (50, 50, 100)
                            frame = cv2.addWeighted(frame, 0.3, final_bg, 0.7, 0)
                            
                            cv2.putText(frame, "🏆 QUIZ COMPLETE! 🏆", (width//2 - 200, height//2 - 100), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)
                            cv2.putText(frame, f"Final Score: {score}/{len(all_questions)}", 
                                       (width//2 - 150, height//2 - 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3)
                            
                            percentage = (score / len(all_questions)) * 100
                            if percentage >= 80:
                                grade_text = "🌟 Excellent! 🌟"
                                grade_color = (0, 255, 0)
                            elif percentage >= 60:
                                grade_text = "👍 Good Job! 👍"
                                grade_color = (0, 255, 255)
                            else:
                                grade_text = "📚 Keep Practicing! 📚"
                                grade_color = (0, 150, 255)
                            
                            cv2.putText(frame, grade_text, (width//2 - 150, height//2 + 50), 
                                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, grade_color, 3)
                            
                            cv2.imshow('🎯 Hand Gesture Quiz - Interactive Learning', frame)
                            cv2.waitKey(4000)  # Show final score for 4 seconds
                            break
                
                # Enhanced UI elements
                # Score display
                score_bg = np.zeros((60, 300, 3), dtype=np.uint8)
                score_bg[:] = (40, 40, 40)
                frame[height-70:height-10, width-310:width-10] = cv2.addWeighted(
                    frame[height-70:height-10, width-310:width-10], 0.5, score_bg, 0.5, 0)
                
                cv2.putText(frame, f"Score: {score}/{len(all_questions)}", 
                           (width-300, height-45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(frame, f"Question: {current_question_index + 1}/{len(all_questions)}", 
                           (width-300, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
                
                # Instructions
                cv2.putText(frame, "🤚 Move your hand to control the ball | Touch answers to select | Press 'q' to quit", 
                           (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.imshow('🎯 Hand Gesture Quiz - Interactive Learning', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
        
        except Exception as e:
            messagebox.showerror("Error", f"Camera error: {str(e)}")
            if 'cap' in locals():
                cap.release()
            cv2.destroyAllWindows()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = QuizApp()
    app.run()