#include <stdio.h>
#include "phylib.h"
#include <stdlib.h>
#include <math.h>
#include <string.h>

int main() {
    // Create two rolling balls for testing
    phylib_object *rollingBallA = (phylib_object *)malloc(sizeof(phylib_object));
    rollingBallA->type = PHYLIB_ROLLING_BALL;
    rollingBallA->obj.rolling_ball.number = 1;
    rollingBallA->obj.rolling_ball.pos.x = 10.0;
    rollingBallA->obj.rolling_ball.pos.y = 20.0;
    rollingBallA->obj.rolling_ball.vel.x = 2.0;
    rollingBallA->obj.rolling_ball.vel.y = 1.0;
    rollingBallA->obj.rolling_ball.acc.x = 0.0;
    rollingBallA->obj.rolling_ball.acc.y = 0.0;

    phylib_object *rollingBallB = (phylib_object *)malloc(sizeof(phylib_object));
    rollingBallB->type = PHYLIB_STILL_BALL;
    // rollingBallB->obj.rolling_ball.number = 2;
    rollingBallB->obj.rolling_ball.pos.x = 15.0;
    rollingBallB->obj.rolling_ball.pos.y = 25.0;
    // rollingBallB->obj.rolling_ball.vel.x = -1.0;
    // rollingBallB->obj.rolling_ball.vel.y = -2.0;
    // rollingBallB->obj.rolling_ball.acc.x = 0.0;
    // rollingBallB->obj.rolling_ball.acc.y = 0.0;

    // Print initial velocities
    printf("Initial Velocities:\n");
    printf("Ball A: (%.2lf, %.2lf)\n", rollingBallA->obj.rolling_ball.vel.x, rollingBallA->obj.rolling_ball.vel.y);
    printf("Ball B: (%.2lf, %.2lf)\n", rollingBallB->obj.rolling_ball.vel.x, rollingBallB->obj.rolling_ball.vel.y);

    // Simulate a collision
    phylib_bounce(&rollingBallA, &rollingBallB);

    // Print velocities after collision
    printf("\nVelocities After Collision:\n");
    if(rollingBallA == NULL){
      printf("IF WAS A HOLE");
    }
    else
    printf("Ball A: (%.2lf, %.2lf)\n", rollingBallA->obj.rolling_ball.vel.x, rollingBallA->obj.rolling_ball.vel.y);
    printf("Ball B: (%.2lf, %.2lf)\n", rollingBallB->obj.rolling_ball.vel.x, rollingBallB->obj.rolling_ball.vel.y);

    // Clean up - free memory
    free(rollingBallA);
    free(rollingBallB);

    return 0;
}

/*
void phylib_print_object( phylib_object *object )
{
  if (object==NULL)
  {
    printf( "NULL;\n" );
    return;
  }

  switch (object->type)
  {
    case PHYLIB_STILL_BALL:
      printf( "STILL_BALL (%d,%6.1lf,%6.1lf)\n",
	      object->obj.still_ball.number,
	      object->obj.still_ball.pos.x,
	      object->obj.still_ball.pos.y );
      break;

    case PHYLIB_ROLLING_BALL:
      printf( "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)\n",
              object->obj.rolling_ball.number,
              object->obj.rolling_ball.pos.x,
              object->obj.rolling_ball.pos.y,
              object->obj.rolling_ball.vel.x,
              object->obj.rolling_ball.vel.y,
              object->obj.rolling_ball.acc.x,
              object->obj.rolling_ball.acc.y );
      break;

    case PHYLIB_HOLE:
      printf( "HOLE (%6.1lf,%6.1lf)\n",
	      object->obj.hole.pos.x,
	      object->obj.hole.pos.y );
      break;

    case PHYLIB_HCUSHION:
      printf( "HCUSHION (%6.1lf)\n",
	      object->obj.hcushion.y );
      break;

    case PHYLIB_VCUSHION:
      printf( "VCUSHION (%6.1lf)\n",
	      object->obj.vcushion.x );
      break;
  }
}

void phylib_print_table( phylib_table *table )
{
  if (!table)
  {
    printf( "NULL\n" );
    return ;
  }

  printf( "time = %6.1lf;\n", table->time );
  for ( int i=0; i<PHYLIB_MAX_OBJECTS; i++ )
  {
    printf( "  [%02d] = ", i );
    phylib_print_object( table->object[i] );
  }

}


int main( int argc, char **argv )
{
  phylib_coord pos, vel, acc;
  phylib_table *table;
  phylib_object *sb;
  phylib_object *rb;

  table = phylib_new_table();

  // create a still ball 1/4 of the way "down" the middle of the table,
  // shift it up, and to the left just a little bit
  pos.x = PHYLIB_TABLE_WIDTH / 2.0 
          - sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  pos.y = PHYLIB_TABLE_WIDTH / 2.0
          - sqrt( PHYLIB_BALL_DIAMETER*PHYLIB_BALL_DIAMETER / 2.0 );
  sb = phylib_new_still_ball( 1, &pos );

  // create a rolling ball 3/4 of the way "down the table,
  // rolling up along the centre
  pos.x = PHYLIB_TABLE_WIDTH / 2.0;
  pos.y = PHYLIB_TABLE_LENGTH - PHYLIB_TABLE_WIDTH / 2.0;
  vel.x = 0.0;
  vel.y = -1000.0; // 1m/s (medium speed)
  acc.x = 0.0;
  acc.y = 180.0;
  rb = phylib_new_rolling_ball( 0, &pos, &vel, &acc );

  phylib_add_object( table, sb );
  phylib_add_object( table, rb );

  phylib_print_table( table );

  
  do
  {
    phylib_table *new = phylib_segment( table );
    phylib_free_table( table );
    table = new;

    phylib_print_table( table );
  } while( table );
}*/

