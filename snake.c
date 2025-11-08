#include "game.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "snake_utils.h"

/* Helper function definitions */
static void set_board_at(game_t *game, unsigned int row, unsigned int col, char ch);
static bool is_tail(char c);
static bool is_head(char c);
static bool is_snake(char c);
static char body_to_tail(char c);
static char head_to_body(char c);
static unsigned int get_next_row(unsigned int cur_row, char c);
static unsigned int get_next_col(unsigned int cur_col, char c);
static void find_head(game_t *game, unsigned int snum);
static char next_square(game_t *game, unsigned int snum);
static void update_tail(game_t *game, unsigned int snum);
static void update_head(game_t *game, unsigned int snum);

/* Task 1 */
 game_t *create_default_game() {
  // TODO: Implement this function.
  // need to save snake struct 
game_t *ptr = malloc(sizeof(game_t)); 

ptr -> board = (char**)malloc(18 * sizeof(char*));



for(int i = 0; i < 18; i++){
    ptr -> board[i] = malloc(22);
    

}

//strcpy all of this
strcpy(ptr -> board[0],  "####################\n");
strcpy(ptr -> board[1], "#                  #\n");
strcpy(ptr -> board[2], "# d>D    *         #\n");
strcpy(ptr -> board[3], "#                  #\n");

strcpy(ptr -> board[4], "#                  #\n");

strcpy(ptr -> board[5],"#                  #\n");



strcpy(ptr -> board[6],"#                  #\n");
strcpy(ptr -> board[7],"#                  #\n");
strcpy(ptr -> board[8],"#                  #\n");
strcpy(ptr -> board[9],"#                  #\n");
strcpy(ptr -> board[10],"#                  #\n");
strcpy(ptr -> board[11],"#                  #\n");
strcpy(ptr -> board[12],"#                  #\n");
strcpy(ptr -> board[13],"#                  #\n");
strcpy(ptr -> board[14],"#                  #\n");
strcpy(ptr -> board[15],"#                  #\n");
strcpy(ptr -> board[16],"#                  #\n");
strcpy(ptr -> board[17], "####################\n");

ptr->snakes = (snake_t*)malloc(1 * sizeof(snake_t));

ptr -> num_rows = 18; 

ptr -> num_snakes = 1;

ptr->snakes[0].tail_row = 2;
  ptr->snakes[0].tail_col = 2;
  ptr->snakes[0].head_row = 2;
  ptr->snakes[0].head_col = 4;
  ptr->snakes[0].live = true;



  return ptr;
}


/* Task 2 */
void free_game(game_t *game) {
// TODO: Implement this function.
free (game -> snakes);
for (int i = 0; i < game->num_rows; i++) {
       free(game->board[i]);
    }
free (game->board); // change variable name

free (game);
  
  return;
}

/* Task 3 */
void print_board(game_t *game, FILE *fp) {
  for (int i = 0; i < game-> num_rows; i++) {
        fprintf(fp, "%s", game->board[i]); //may need to change variable names
    }
  return;
}

/*
  Saves the current game into filename. Does not modify the game object.
  (already implemented for you).
*/
void save_board(game_t *game, char *filename) {
  FILE *f = fopen(filename, "w");
  print_board(game, f);
  fclose(f);
}

/* Task 4.1 */

/*
  Helper function to get a character from the board
  (already implemented for you).
*/
char get_board_at(game_t *game, unsigned int row, unsigned int col) { return game->board[row][col]; }

/*
  Helper function to set a character on the board
  (already implemented for you).
*/
static void set_board_at(game_t *game, unsigned int row, unsigned int col, char ch) {
  game->board[row][col] = ch;
}

/*
  Returns true if c is part of the snake's tail.
  The snake consists of these characters: "wasd"
  Returns false otherwise.
*/
static bool is_tail(char c) {
  // TODO: Implement this function.
  //int len = 4;
  char tailarray[] = "wasd";
  for(int i = 0; i< 4; i++){
    if (c == tailarray[i] ){
        return true;
    }

  }
  return false;
}

/*
  Returns true if c is part of the snake's head.
  The snake consists of these characters: "WASDx"
  Returns false otherwise.
*/
static bool is_head(char c) {
  // TODO: Implement this function.
  //int len = 5;
  char headarray[] = "WASDx";
  for(int i = 0; i< 5; i++){
    if (c == headarray[i] ){
        return true;
    }

  }
  return false;
}

/*
  Returns true if c is part of the snake.
  The snake consists of these characters: "wasd^<v>WASDx"
*/
static bool is_snake(char c) {
  // TODO: Implement this function.
  int len = strlen("wasd^<v>WASDx");
  char bodyarray[] = "wasd^<v>WASDx";
  for(int i = 0; i< len; i++){
    if (c == bodyarray[i] ){
        return true;
    }

  }
  return false;

}

/*
  Converts a character in the snake's body ("^<v>")
  to the matching character representing the snake's
  tail ("wasd").
*/
static char body_to_tail(char c) {
  // TODO: Implement this function.
  if (c == '^') {
        return 'w';
    } else if (c == '<') {
        return 'a';
    } else if (c == 'v') {
        return 's';
    } else if (c == '>') {
        return 'd';
    }
  return '?';
}

/*
  Converts a character in the snake's head ("WASD")
  to the matching character representing the snake's
  body ("^<v>").
*/
static char head_to_body(char c) {
  // TODO: Implement this function.
  if (c == 'W') {
        return '^';
    } else if (c == 'A') {
        return '<';
    } else if (c == 'S') {
        return 'v';
    } else if (c == 'D') {
        return '>';
    }
  return '?';
}

/*
  Returns cur_row + 1 if c is 'v' or 's' or 'S'.
  Returns cur_row - 1 if c is '^' or 'w' or 'W'.
  Returns cur_row otherwise.
*/
static unsigned int get_next_row(unsigned int cur_row, char c) {
  if (c == 'v' || c == 's'|| c== 'S'){
    cur_row += 1;
  } else if (c == '^' || c == 'w' || c == 'W'){
    cur_row -= 1;
  }
  return cur_row;
}

/*
  Returns cur_col + 1 if c is '>' or 'd' or 'D'.
  Returns cur_col - 1 if c is '<' or 'a' or 'A'.
  Returns cur_col otherwise.
*/
static unsigned int get_next_col(unsigned int cur_col, char c) {
  // TODO: Implement this function.
    if (c == '>' || c == 'd'|| c == 'D'){
    cur_col += 1;
  } else if (c == '<' || c == 'a' || c == 'A'){
    cur_col -= 1;
  }
  return cur_col;
}

/*
  Task 4.2

  Helper function for update_game. Return the character in the cell the snake is moving into.

  This function should not modify anything.
*/
static char next_square(game_t *game, unsigned int snum) {
  // TODO: Implement this function.
  /// FIX THIS FUNCTION

  char cell = get_board_at(game, game -> snakes[snum].head_row, game -> snakes[snum].head_col) ;//game_t *game proper pass???
  unsigned int nextrow = get_next_row(game -> snakes[snum].head_row, cell); 
  unsigned int  nextcol = get_next_col(game -> snakes[snum].head_col, cell);
  char move =  get_board_at(game, nextrow, nextcol) ;
  return move;
  return '?';
}

/*
  Task 4.3

  Helper function for update_game. Update the head...

  ...on the board: add a character where the snake is moving

  ...in the snake struct: update the row and col of the head

  Note that this function ignores food, walls, and snake bodies when moving the head.
*/
static void update_head(game_t *game, unsigned int snum) {//update head or body too? {
  // TODO: Implement this function.
 
  unsigned int headrow = game -> snakes[snum].head_row; 
  unsigned int headcol = game -> snakes[snum].head_col; 
  char c = get_board_at(game, headrow, headcol);
  unsigned new_row = get_next_row( headrow,  c);
  unsigned new_col = get_next_col(headcol, c);  //this function is wrond
  set_board_at(game, headrow, headcol, c);
  game -> snakes[snum].head_row = new_row;
  game -> snakes[snum].head_col = new_col;




  
  
    return;
}

/*
  Task 4.4

  Helper function for update_game. Update the tail...

  ...on the board: blank out the current tail, and change the new
  tail from a body character (^<v>) into a tail character (wasd)

  ...in the snake struct: update the row and col of the tail
*/
static void update_tail(game_t *game, unsigned int snum) {
  // TODO: Implement this function.
  //FIX THIS FUNCTION
  unsigned int tailrow = game -> snakes[snum].tail_row; 
  unsigned int tailcol = game -> snakes[snum].tail_col; 
  char c = get_board_at(game, tailrow, tailcol);
  char blank = ' ';
  unsigned int new_tailrow = get_next_row( tailrow,  c);
  unsigned int new_tailcol = get_next_col(tailcol, c);
  set_board_at(game, new_tailrow, new_tailcol, c);
  set_board_at(game, tailrow, tailcol, blank);
  game -> snakes[snum].head_row = new_tailrow;
  game -> snakes[snum].head_col = new_tailcol;
  return;
}

/* Task 4.5 */
void update_game(game_t *game, int (*add_food)(game_t *game)) {
  // TODO: Implement this function.
  unsigned int length = game -> num_snakes;
  for (unsigned int i = 0; i < length; i++){ 
    char next = next_square(game, i);
    if (next == '>'|| next == '^'||next == '<'|| next == 'v'||next == '#'){
      char dead = 'x';
      unsigned int headrow = game -> snakes[i].head_row;  //stores the location of the old head
      unsigned int headcol = game -> snakes[i].head_col; //stores the loaction of the old head
      char head = get_board_at(game, headrow, headcol); 
      char new_body = head_to_body(head);  //tells me what body char to use
      set_board_at(game, headrow, headcol, new_body); //sets the board with the new body character
      update_head(game, i); 
      set_board_at(game, game -> snakes[i].head_row,   game -> snakes[i].head_col, dead); //sets the head to dead
      update_tail(game, i); 
      } 
    else if (next == '*'){
      unsigned int headrow = game -> snakes[i].head_row;  //stores the location of the old head
      unsigned int headcol = game -> snakes[i].head_col; //stores the loaction of the old head
      char head = get_board_at(game, headrow, headcol); 
      char body = head_to_body(head);
      set_board_at(game, game -> snakes[i].head_row,   game -> snakes[i].head_col, body);
      update_head(game, i); 
      add_food(game);
      // new fruit on the map
      
      }
    else{ 
      unsigned int headrow = game -> snakes[i].head_row;  //stores the location of the old head
      unsigned int headcol = game -> snakes[i].head_col; 
      char head = get_board_at(game, headrow, headcol); 
      char body = head_to_body(head);
      set_board_at(game, headrow, headcol, body);

      update_head(game, i); 
      update_tail(game, i);
    }
    }
  return;
}

/* Task 5.1 */
char *read_line(FILE *fp) {
  // TODO: Implement this function.
if (fp == NULL) {
    return NULL;
  }
  char stringarray [20];  // creates ample amount of space for the first line
  if (fgets(stringarray, 20, fp) == NULL) {
        return NULL;  // Handle end of file or error
    }
  fgets(stringarray,20,fp); // need to create an another error exception

  long unsigned int length = strlen(stringarray) -1;

  char *ptr = malloc(length + 1);

  char restorearray[length + 1];
  
  for ( int i = 0; i < length; i ++){
    restorearray[i] = stringarray[i];
  }
  restorearray[length -1] = '\0';

  strcpy(ptr, restorearray); 

  return ptr;

}

/* Task 5.2 */
game_t *load_board(FILE *fp) {
  // TODO: Implement this function.
  return NULL;
}

/*
  Task 6.1

  Helper function for initialize_snakes.
  Given a snake struct with the tail row and col filled in,
  trace through the board to find the head row and col, and
  fill in the head row and col in the struct.
*/
static void find_head(game_t *game, unsigned int snum) {
  // TODO: Implement this function.

  //CHECK THIS FUCNTION !!!!!!!!!
  //!!!!!!!!!!
  char curr = get_board_at(game, game -> snakes[snum].tail_row, game-> snakes[snum].tail_col);
  unsigned int headrow = game -> snakes[snum].tail_row;
  unsigned int headcol = game-> snakes[snum].tail_col;
  while( is_head(curr) == false ){
    headrow = get_next_row(headrow, curr);
    headcol = get_next_col(headcol, curr);
    curr = get_board_at(game, headrow, headcol);

  }
  game -> snakes[snum].head_row = headrow; 
  game-> snakes[snum].head_col = headcol;


  return;
}

/* Task 6.2 */
game_t *initialize_snakes(game_t *game) {
  // TODO: Implement this function.
  // need to FIX THIS METHOD!!!!!!!!!!
  long unsigned int col_len = strlen(game -> board[0]);
  game -> num_snakes = 0;
  for ( unsigned int i = 0; i < game -> num_rows; i ++){
    for (unsigned int j = 0; j < col_len; j++){ //fix this method
        if (is_tail (game -> board[i][j]) == true){
            game -> snakes[game -> num_snakes].tail_row = i;
            game -> snakes[game -> num_snakes].tail_col = j;
            // check if snake is alive
            find_head(game, game-> num_snakes);
            game -> num_snakes += 1; 
            //need to update snake struct
        }
    }
  }
  return NULL;
}
