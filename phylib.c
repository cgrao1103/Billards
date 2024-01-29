#include "phylib.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>


phylib_object *phylib_new_still_ball( unsigned char number, phylib_coord *pos ){
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
    if(newObject == NULL){
        return NULL;
    }
    newObject->type = PHYLIB_STILL_BALL;
    newObject->obj.still_ball.number = number;
    newObject->obj.still_ball.pos = *pos;
    return newObject;
}

phylib_object *phylib_new_rolling_ball( unsigned char number, phylib_coord *pos, phylib_coord *vel,
phylib_coord *acc ){
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
    if(newObject == NULL){
        return NULL;
    }
    newObject->type = PHYLIB_ROLLING_BALL;
    newObject->obj.rolling_ball.number = number;
    newObject->obj.rolling_ball.pos = *pos;
    newObject->obj.rolling_ball.vel = *vel;
    newObject->obj.rolling_ball.acc = *acc;
    return newObject;

}

phylib_object *phylib_new_hole( phylib_coord *pos ){
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
    if(newObject == NULL){
        return NULL;
    }
    newObject->type = PHYLIB_HOLE;
    newObject->obj.hole.pos = *pos;
    return newObject;
}

phylib_object *phylib_new_hcushion( double y ){
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
    if(newObject == NULL){
        return NULL;
    }
    newObject->type = PHYLIB_HCUSHION;
    newObject->obj.hcushion.y = y;
    return newObject;
}
phylib_object *phylib_new_vcushion( double x ){
    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
    if(newObject == NULL){
        return NULL;
    }
    newObject->type = PHYLIB_VCUSHION;
    newObject->obj.vcushion.x = x;
    return newObject;
}

phylib_table *phylib_new_table( void ){
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    
    newTable->time=0.0;
    if(newTable == NULL){
        return NULL;
    }
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        newTable->object[i] = NULL;
    }
    newTable->object[0] = phylib_new_hcushion(0.0);
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    newTable->object[2] = phylib_new_vcushion(0.0);
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0});
    newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH / 2.0});
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH});
    newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH});
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0});
    newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH / 2.0});
    
    return newTable;
}

void phylib_copy_object( phylib_object **dest, phylib_object **src ){
    if (*src == NULL) {
        *dest = NULL;
    } 
    
    else {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        if (*dest != NULL) {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }
}

phylib_table *phylib_copy_table(phylib_table *table) {
    if (table == NULL) {
        return NULL;
    }

    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    if (newTable == NULL) {
        return NULL;
    }

    newTable->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] != NULL) {
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
        } else {
            newTable->object[i] = NULL;
        }
    }

    return newTable;
}


void phylib_add_object( phylib_table *table, phylib_object *object ){
    if (table == NULL || object == NULL) {
        return;
    }
        
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            return;
        }
    }
    
}

void phylib_free_table( phylib_table *table ){
if (table == NULL) {
        return;
    }
for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
    
        
    if (table->object[i] != NULL) {
    
        free(table->object[i]);
        table->object[i] = NULL;
    
        }}
    free(table);

}

phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord result;
    result.x=c1.x-c2.x;
    result.y=c1.y-c2.y;
    return result;
}

double phylib_length( phylib_coord c ){
    double vector = sqrt(c.x*c.x + c.y*c.y);
    return vector;
}

double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double dot = a.x*b.x + b.y*a.y;
    return dot;
}


double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    if (obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0; // obj1 is not a PHYLIB_ROLLING_BALL
    }

    phylib_rolling_ball *rollingBall1 = &(obj1->obj.rolling_ball);
    phylib_coord pos1 = rollingBall1->pos;
    double distance = -1.0;

    switch (obj2->type) {
        case PHYLIB_ROLLING_BALL:
        case PHYLIB_STILL_BALL: {
            phylib_coord pos2 = (obj2->type == PHYLIB_ROLLING_BALL) ? obj2->obj.rolling_ball.pos : obj2->obj.still_ball.pos;
            distance = sqrt(pow(pos1.x - pos2.x, 2) + pow(pos1.y - pos2.y, 2)) - PHYLIB_BALL_DIAMETER;
            break;
        }
        case PHYLIB_HOLE: {
            phylib_coord pos2 = obj2->obj.hole.pos;
            distance = sqrt(pow(pos1.x - pos2.x, 2) + pow(pos1.y - pos2.y, 2)) - PHYLIB_HOLE_RADIUS;
            break;
        }
        case PHYLIB_HCUSHION: {
            double ballRadius = PHYLIB_BALL_RADIUS;
            double cushionY = obj2->obj.hcushion.y;
            distance = fabs(rollingBall1->pos.y - cushionY) - ballRadius;
            break;
        }
        case PHYLIB_VCUSHION: {
            double ballRadius = PHYLIB_BALL_RADIUS;
            double cushionX = obj2->obj.vcushion.x;
            distance = fabs(rollingBall1->pos.x - cushionX) - ballRadius;
            break;
        }
    }

    return distance;
}


phylib_coord phylib_normalize(phylib_coord c) {
    double length = sqrt(c.x * c.x + c.y * c.y);
    phylib_coord result;
    if (length > 0.0) {
        result.x = c.x / length;
        result.y = c.y / length;
    } else {
        result.x = 0.0;
        result.y = 0.0;
    }
    return result;
}

phylib_coord phylib_scalar_multiply(double scalar, phylib_coord c) {
    phylib_coord result;
    result.x = scalar * c.x;
    result.y = scalar * c.y;
    return result;
}


void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL) {
        return; 
    }

    

//position p1 +v1*t + 0.5(a1*t*t)
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * (old->obj.rolling_ball.acc.x * time * time);
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * (old->obj.rolling_ball.acc.y * time * time);

//velocity - v=v1=a1 * t
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x * time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y * time;


//change sign 
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0) {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0) {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

unsigned char phylib_stopped( phylib_object *object ){
    if (object->type != PHYLIB_ROLLING_BALL || object == NULL){
        return 0;
    }

    double speed = sqrt(object->obj.rolling_ball.vel.x * object->obj.rolling_ball.vel.x + object->obj.rolling_ball.vel.y * object->obj.rolling_ball.vel.y);

    if (speed < PHYLIB_VEL_EPSILON) {
        object->type= PHYLIB_STILL_BALL;
        return 1; 
    }
    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    // Check if object a is a PHYLIB_ROLLING_BALL
    if (*a == NULL || (*a)->type != PHYLIB_ROLLING_BALL) {
        return; // a is not a PHYLIB_ROLLING_BALL, do nothing
    }
    
    phylib_coord r_ab ;
    // Check the type of object b
    switch ((*b)->type) {

        case PHYLIB_HCUSHION:
            // Case 1: b is a HCUSHION
            // Reverse y velocity and y acceleration of a
            (*a)->obj.rolling_ball.vel.y = -(*a)->obj.rolling_ball.vel.y;
            (*a)->obj.rolling_ball.acc.y = -(*a)->obj.rolling_ball.acc.y;
            break;

        case PHYLIB_VCUSHION:
            // Case 2: b is a VCUSHION
            // Reverse x velocity and x acceleration of a
            (*a)->obj.rolling_ball.vel.x = -(*a)->obj.rolling_ball.vel.x;
            (*a)->obj.rolling_ball.acc.x = -(*a)->obj.rolling_ball.acc.x;
            break;

        case PHYLIB_HOLE:
            // Case 3: b is a HOLE
            // Free memory of a and set it to NULL
            free(*a);
            *a = NULL;
            break;

        case PHYLIB_STILL_BALL:
            // Case 4: b is a STILL_BALL
            // Upgrade STILL_BALL to ROLLING_BALL and proceed to CASE 5
            (*b)->type = PHYLIB_ROLLING_BALL;
            // Fall through to CASE 5 (no break statement)

        case PHYLIB_ROLLING_BALL:
            // Case 5: b is a ROLLING_BALL
            // Calculate intermediate values
            
            
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            phylib_coord v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            phylib_coord n = phylib_normalize(r_ab);
            double v_rel_n = phylib_dot_product(v_rel, n);
            // Update velocities of ball a
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;

            // Update velocities of ball b
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // Compute speeds
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            // Apply drag if speed is greater than PHYLIB_VEL_EPSILON
            if (speed_a > PHYLIB_VEL_EPSILON) {
                phylib_coord acc_a = phylib_scalar_multiply(-1.0 / speed_a, (*a)->obj.rolling_ball.vel);
                (*a)->obj.rolling_ball.acc = phylib_scalar_multiply(PHYLIB_DRAG, acc_a);
            }

            if (speed_b > PHYLIB_VEL_EPSILON) {
                phylib_coord acc_b = phylib_scalar_multiply(-1.0 / speed_b, (*b)->obj.rolling_ball.vel);
                (*b)->obj.rolling_ball.acc = phylib_scalar_multiply(PHYLIB_DRAG, acc_b);
            }

            break;
    }
}

unsigned char phylib_rolling(phylib_table *t) {
    if (t == NULL) {
        return 0; // No table, no rolling balls
    }

    unsigned char rolling_count = 0;

    // Loop through the objects in the table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        phylib_object *obj = t->object[i];

        // Check if the object is a ROLLING_BALL
        if (obj != NULL && obj->type == PHYLIB_ROLLING_BALL) {
            rolling_count++;
        }
    }

    return rolling_count;
}

phylib_table* phylib_segment(phylib_table *table) {
    if (table == NULL) {
        return NULL; // No table, return NULL
    }

    // Check if there are any ROLLING_BALLs on the table
    unsigned char rolling_count = phylib_rolling(table);
    if (rolling_count == 0) {
        return NULL; // No rolling balls, return NULL
    }

    // Create a copy of the table
    phylib_table *segment_table = phylib_copy_table(table);

    // Initialize time variable
    double time = PHYLIB_SIM_RATE;

    // Loop until PHYLIB_MAX_TIME is reached
    while (time <= PHYLIB_MAX_TIME) {
        // Loop through the objects in the segment table
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            phylib_object *obj = segment_table->object[i];

            // Check if the object is a ROLLING_BALL
            if (obj != NULL && obj->type == PHYLIB_ROLLING_BALL) {
                // Update the position of the rolling ball
                phylib_object *new_obj = phylib_new_rolling_ball(
                    obj->obj.rolling_ball.number,
                    &obj->obj.rolling_ball.pos,
                    &obj->obj.rolling_ball.vel,
                    &obj->obj.rolling_ball.acc
                );
                phylib_roll(new_obj, obj, time);

                // Check if the ball has stopped
                if (phylib_stopped(new_obj)) {
                    free(new_obj);
                    return segment_table; // Ball has stopped, return the segment table
                }

                // Check for collisions with other objects
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (i != j) { // Avoid self-collision
                        phylib_object *other_obj = segment_table->object[j];

                        // Check if there is a collision
                        if (other_obj != NULL && phylib_distance(new_obj, other_obj) < 0.0) {
                            // Apply bounce and return the segment table
                            phylib_bounce(&new_obj, &other_obj);
                            free(new_obj);
                            return segment_table;
                        }
                    }
                }

                // Update the object in the segment table
                phylib_copy_object(&(segment_table->object[i]), &new_obj);
                free(new_obj);
            }
        }

        // Increment time
        time += PHYLIB_SIM_RATE;
    }

    return segment_table; // PHYLIB_MAX_TIME reached, return the segment table
}

