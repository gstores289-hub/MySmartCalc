from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import math
import re

class CalculatorApp(App):
    def build(self):
        self.history = []
        main_layout = BoxLayout(orientation="vertical", padding=2, spacing=2)

        self.solution = TextInput(
            multiline=False, readonly=True, halign="right", font_size=90,
            background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1),
            size_hint=(1, 0.3), padding=[10, 40]
        )
        main_layout.add_widget(self.solution)

        # أضفت زر "Exit" في الشبكة لتجربة رسالة الوداع
        buttons = [
            ["sin", "cos", "tan", "/"],
            ["√", "^", "ln", "*"],
            ["(", ")", "π", "-"],
            ["7", "8", "9", "+"],
            ["4", "5", "6", "DEL"],
            ["1", "2", "3", "C"],
            ["Hist", "0", "Exit", "="] # استبدلنا النقطة بـ Exit للتجربة
        ]

        grid_layout = GridLayout(cols=4, spacing=2)

        for row in buttons:
            for label in row:
                bg_color = (0.1, 0.1, 0.1, 1)
                txt_color = (1, 1, 1, 1)

                if label == "=":
                    bg_color = (0.63, 0.55, 0.35, 1)
                elif label in ["C", "DEL", "Hist", "Exit"]:
                    bg_color = (0.2, 0.2, 0.2, 1)
                    txt_color = (0.83, 0.64, 0.45, 1)
                elif not label.isdigit() and label != ".":
                    txt_color = (0.83, 0.64, 0.45, 1)

                btn = Button(
                    text=label, background_normal='', 
                    background_color=bg_color, color=txt_color,
                    font_size=45, bold=True
                )
                btn.bind(on_press=self.on_button_press)
                grid_layout.add_widget(btn)

        main_layout.add_widget(grid_layout)
        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            self.solution.text = ""
        elif button_text == "DEL":
            self.solution.text = current[:-1]
        elif button_text == "Hist":
            if self.history: self.solution.text = self.history[-1].split('=')[1]
        elif button_text == "Exit":
            self.show_farewell()
        elif button_text == "=":
            self.on_solution()
        else:
            if button_text in ["sin", "cos", "tan", "√", "ln"]:
                self.solution.text += button_text + "("
            else:
                self.solution.text += button_text

    def show_farewell(self):
        # عرض الرسالة التي طلبتها
        self.solution.font_size = 40
        self.solution.text = "صالح يرحب بكم\nشكراً للاستخدام"
        # إغلاق التطبيق بعد ثانيتين
        Clock.schedule_once(lambda dt: self.stop(), 2)

    def on_solution(self):
        text = self.solution.text
        try:
            temp_text = re.sub(r'(\d)(\(|sin|cos|tan|√|ln|π)', r'\1*\2', text)
            expr = temp_text.replace('√', 'math.sqrt').replace('ln', 'math.log').replace('^', '**')
            expr = expr.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan')
            expr = expr.replace('π', 'math.pi')
            expr += ')' * (expr.count('(') - expr.count(')'))
            
            result_val = eval(expr)
            res = f"{result_val:.10f}".rstrip('0').rstrip('.')
            self.history.append(f"{text}={res}")
            self.solution.text = res
        except:
            self.solution.text = "Error"

if __name__ == "__main__":
    CalculatorApp().run()
