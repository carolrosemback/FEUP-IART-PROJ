import timeit
import numpy


def copyBoard(board):
    board_aux = []

    board_aux = []
    for row in range(4):
        row_aux = []
        for col in range(4):
            row_aux.append(board[row][col]) # add element
        board_aux.append(row_aux) # add row
        
    return board_aux                

def copyBoards(boards):
        
        result = []
        for homeboard in range(2):
            homeboard_aux  = []
            for board in range(2):
                board_aux = []
                for row in range(4):
                    row_aux = []
                    for col in range(4):
                        row_aux.append(boards[homeboard][board][row][col]) # add element
                    board_aux.append(row_aux) # add row
                homeboard_aux.append(board_aux) # add board
            result.append(homeboard_aux) # add homeboard
            
        return result                
                        

def main():
    
    boards = [[[['W', 'W', 'W', 'W'],
                  [' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' '],
                  ['B', 'B', 'B', 'B']],
    
                 [['W', 'W', 'W', 'W'],
                  [' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' '],
                  ['B', 'B', 'B', 'B']]],
    
                [[['W', 'W', 'W', 'W'],
                  [' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' '],
                  ['B', 'B', 'B', 'B']],
    
                 [['W', 'W', 'W', 'W'],
                  [' ', ' ', ' ', ' '],
                  [' ', ' ', ' ', ' '],
                  ['B', 'B', 'B', 'B']]]]
    
    
    # board_string = "[[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]],[[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']],[['W', 'W', 'W', 'W'],[' ', ' ', ' ', ' '],[' ', ' ', ' ', ' '],['B', 'B', 'B', 'B']]]]"
    
    lista = [12341,23412351,2361236,12341,324123,5123,4123,413613,1234,123,41324,1234123,61,237,57,45674,67467,4674,5736,2413,4,1235,436,5477665845,945673,623,5432,52,3452345,2345,2345,23452346,565235423,45234,523,45234,5,23452345,2345234,65,6345,623,44,13,68,795679,56795670,58097,680,69856,875687,567856,7856,8756,7856,7856,87,4567,34,52,7,5679,70,8790,7890,7890,9,41234,1234,1234,1234,1234]
    
    array = numpy.array([12341,23412351,2361236,12341,324123,5123,4123,413613,1234,123,41324,1234123,61,237,57,45674,67467,4674,5736,2413,4,1235,436,5477665845,945673,623,5432,52,3452345,2345,2345,23452346,565235423,45234,523,45234,5,23452345,2345234,65,6345,623,44,13,68,795679,56795670,58097,680,69856,875687,567856,7856,8756,7856,7856,87,4567,34,52,7,5679,70,8790,7890,7890,9,41234,1234,1234,1234,1234])
    
    start_time1 = timeit.default_timer()
    best_move = sorted(lista) #ascending order, for black
    elapsed = timeit.default_timer() - start_time1
    print("1:4 CopyBoard Elapsed Time: ", elapsed)

    
<<<<<<< HEAD
=======

>>>>>>> 8676893f9b47011d5940770f32614240c8af8628



main()