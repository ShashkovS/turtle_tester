Библиотека для тестирования в ejudge задач по turtle
========================

Примеры запросов

.. code-block:: bash

          import turtle_tester as turtle
          T = Turtle() 
          T.pendown()   
          T.forward(50) 
          T.left(90)    
          T.forward(50) 
          T.left(90)    
          T.forward(50) 
          T.left(90)    
          T.forward(50) 
          T.penup()     
          T.forward(100)
          T.hideturtle()
          turtle.mainloop()  
          
          
          (  +0.00,   +0.00) -> ( +50.00,   +0.00)
          ( +50.00,   +0.00) -> ( +50.00,  +50.00)
          ( +50.00,  +50.00) -> (  +0.00,  +50.00)
          (  +0.00,  +50.00) -> (  -0.00,   +0.00)