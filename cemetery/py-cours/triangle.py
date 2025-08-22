import turtle

def sierpinski(t, length, depth):
    if depth == 0:
        for _ in range(3):
            t.forward(length)
            t.left(120)
    else:
        sierpinski(t, length / 2, depth - 1)
        t.forward(length / 2)
        sierpinski(t, length / 2, depth - 1)
        t.backward(length / 2)
        t.left(60)
        t.forward(length / 2)
        t.right(60)
        sierpinski(t, length / 2, depth - 1)
        t.left(60)
        t.backward(length / 2)
        t.right(60)

# Configuration de l'écran Turtle
window = turtle.Screen()
window.bgcolor("black")

# Configuration de la tortue
t = turtle.Turtle()
t.speed(0)
t.color("white")
t.penup()
t.goto(-200, -150)
t.pendown()

# Appel (alo, a l'huile 🤣) de la fonction récursive
sierpinski(t, 400, 4)

t.hideturtle()
turtle.done()
