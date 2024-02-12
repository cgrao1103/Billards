#include "phylib.h"
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* This function will allocate memory for a new phylib_object, set its type to
PHYLIB_STILL_BALL and transfer the information provided in the function parameters into the
structure */
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos)
{

    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    if (newObject == NULL)
    {
        return NULL;
    }

    newObject->type = PHYLIB_STILL_BALL;
    newObject->obj.still_ball.number = number;
    newObject->obj.still_ball.pos = *pos;

    return newObject;
}

/* These functions will do the same thing as the phylib_new_still_ball function for their
respective structures. */
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel,
                                       phylib_coord *acc)
{

    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    if (newObject == NULL)
    {
        return NULL;
    }

    newObject->type = PHYLIB_ROLLING_BALL;
    newObject->obj.rolling_ball.number = number;
    newObject->obj.rolling_ball.pos = *pos;
    newObject->obj.rolling_ball.vel = *vel;
    newObject->obj.rolling_ball.acc = *acc;

    return newObject;
}

phylib_object *phylib_new_hole(phylib_coord *pos)
{

    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    if (newObject == NULL)
    {
        return NULL;
    }

    newObject->type = PHYLIB_HOLE;
    newObject->obj.hole.pos = *pos;

    return newObject;
}

phylib_object *phylib_new_hcushion(double y)
{

    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    if (newObject == NULL)
    {
        return NULL;
    }

    newObject->type = PHYLIB_HCUSHION;
    newObject->obj.hcushion.y = y;

    return newObject;
}

phylib_object *phylib_new_vcushion(double x)
{

    phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));

    if (newObject == NULL)
    {
        return NULL;
    }

    newObject->type = PHYLIB_VCUSHION;
    newObject->obj.vcushion.x = x;

    return newObject;
}

/*  This function will allocate memory for a table structure, returning NULL if the memory
allocation fails. */
phylib_table *phylib_new_table(void)
{

    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    newTable->time = 0.0;

    if (newTable == NULL)
    {
        return NULL;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {
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

/* This function should allocate new memory for a phylib_object. Save the address of that
object at the location pointed to by dest, and copy over the contents of the object from the
location pointed to by src. */
void phylib_copy_object(phylib_object **dest, phylib_object **src)
{

    if (*src == NULL)
    {
        *dest = NULL;
    }

    else
    {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        if (*dest != NULL)
        {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }
}

/* This function should allocate memory for a new phylib_table, returning NULL if the malloc
fails. Then the contents pointed to by table should be copied to the new memory location and
the address returned. */
phylib_table *phylib_copy_table(phylib_table *table)
{

    if (table == NULL)
    {
        return NULL;
    }

    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));

    if (newTable == NULL)
    {
        return NULL;
    }

    newTable->time = table->time;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {
        if (table->object[i] != NULL)
        {
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
        }
        else
        {
            newTable->object[i] = NULL;
        }
    }

    return newTable;
}

/* This function should iterate over the object array in the table until it finds a NULL pointer. It
should then assign that pointer to be equal to the address of object. */
void phylib_add_object(phylib_table *table, phylib_object *object)
{

    if (table == NULL || object == NULL)
    {
        return;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {
        if (table->object[i] == NULL)
        {
            table->object[i] = object;
            return;
        }
    }
}

/* This function should free every non- NULL pointer in the object array of table. It should then
also free table as well. */
void phylib_free_table(phylib_table *table)
{

    if (table == NULL)
    {
        return;
    }

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i)
    {
        if (table->object[i] != NULL)
        {
            free(table->object[i]);
            table->object[i] = NULL;
        }
    }

    free(table);
}

/* This function should return the difference between c1 and c2. */
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2)
{
    phylib_coord result;
    result.x = c1.x - c2.x;
    result.y = c1.y - c2.y;
    return result;
}

/* This function should return the length of the vector/coordinate c. */
double phylib_length(phylib_coord c)
{
    double vector = sqrt(c.x * c.x + c.y * c.y);
    return vector;
}

/* This function should compute the dot-product between two vectors */
double phylib_dot_product(phylib_coord a, phylib_coord b)
{
    double dot = a.x * b.x + b.y * a.y;
    return dot;
}

/* This function should calculate the distance between two objects, obj1 and obj2. */
double phylib_distance(phylib_object *obj1, phylib_object *obj2)
{

    // obj1 is not a PHYLIB_ROLLING_BALL
    if (obj1->type != PHYLIB_ROLLING_BALL)
    {
        return -1.0;
    }

    phylib_rolling_ball *rollingBall1 = &(obj1->obj.rolling_ball);
    phylib_coord pos1 = rollingBall1->pos;
    double distance = -1.0;

    switch (obj2->type)
    {
    case PHYLIB_ROLLING_BALL:
    case PHYLIB_STILL_BALL:
    {
        phylib_coord pos2 = (obj2->type == PHYLIB_ROLLING_BALL) ? obj2->obj.rolling_ball.pos : obj2->obj.still_ball.pos;
        distance = sqrt(pow(pos1.x - pos2.x, 2) + pow(pos1.y - pos2.y, 2)) - PHYLIB_BALL_DIAMETER;
        break;
    }

    case PHYLIB_HOLE:
    {
        phylib_coord pos2 = obj2->obj.hole.pos;
        distance = sqrt(pow(pos1.x - pos2.x, 2) + pow(pos1.y - pos2.y, 2)) - PHYLIB_HOLE_RADIUS;
        break;
    }

    case PHYLIB_HCUSHION:
    {
        double ballRadius = PHYLIB_BALL_RADIUS;
        double cushionY = obj2->obj.hcushion.y;
        distance = fabs(rollingBall1->pos.y - cushionY) - ballRadius;
        break;
    }

    case PHYLIB_VCUSHION:
    {
        double ballRadius = PHYLIB_BALL_RADIUS;
        double cushionX = obj2->obj.vcushion.x;
        distance = fabs(rollingBall1->pos.x - cushionX) - ballRadius;
        break;
    }
    }

    return distance;
}

/* The function that calculates the length on requirements */
phylib_coord phylibNor(phylib_coord c)
{

    double length = sqrt(c.x * c.x + c.y * c.y);
    phylib_coord result;

    result.x = c.x / length;
    result.y = c.y / length;

    return result;
}

/* This function updates a new phylib_object that represents the old phylib_object after it
has rolled for a period of time. */
void phylib_roll(phylib_object *new, phylib_object *old, double time)
{

    if (new == NULL || old == NULL || new->type != PHYLIB_ROLLING_BALL || old->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    // position p1 +v1*t + 0.5(a1*t*t)
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x *time + 0.5 * (old->obj.rolling_ball.acc.x * time * time);
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y *time + 0.5 * (old->obj.rolling_ball.acc.y * time * time);

    // velocity - v=v1=a1 * t
    new->obj.rolling_ball.vel.x = old->obj.rolling_ball.vel.x + old->obj.rolling_ball.acc.x *time;
    new->obj.rolling_ball.vel.y = old->obj.rolling_ball.vel.y + old->obj.rolling_ball.acc.y *time;

    // change sign
    if ((new->obj.rolling_ball.vel.x * old->obj.rolling_ball.vel.x) < 0)
    {
        new->obj.rolling_ball.vel.x = 0.0;
        new->obj.rolling_ball.acc.x = 0.0;
    }

    if ((new->obj.rolling_ball.vel.y * old->obj.rolling_ball.vel.y) < 0)
    {
        new->obj.rolling_ball.vel.y = 0.0;
        new->obj.rolling_ball.acc.y = 0.0;
    }
}

/* This function will check whether a ROLLING_BALL has stopped, and if it has, will convert it to a
STILL_BALL. */
unsigned char phylib_stopped(phylib_object *object)
{

    if (object->type != PHYLIB_ROLLING_BALL || object == NULL)
    {
        return 0;
    }

    double speed = sqrt(object->obj.rolling_ball.vel.x * object->obj.rolling_ball.vel.x + object->obj.rolling_ball.vel.y * object->obj.rolling_ball.vel.y);

    if (speed < PHYLIB_VEL_EPSILON)
    {
        object->type = PHYLIB_STILL_BALL;
        return 1;
    }

    return 0;
}

// Helper function to handle bouncing off HCUSHION and VCUSHION
void handleCushionBounce(phylib_object *a, phylib_object *b)
{
    if (b->type == PHYLIB_HCUSHION)
    {
        a->obj.rolling_ball.vel.y = -a->obj.rolling_ball.vel.y;
        a->obj.rolling_ball.acc.y = -a->obj.rolling_ball.acc.y;
    }
    else if (b->type == PHYLIB_VCUSHION)
    {
        a->obj.rolling_ball.vel.x = -a->obj.rolling_ball.vel.x;
        a->obj.rolling_ball.acc.x = -a->obj.rolling_ball.acc.x;
    }
}

// Helper function to handle bouncing off ROLLING_BALL
void handleRollingBallBounce(phylib_object *a, phylib_object *b)
{
    phylib_coord r_ab = phylib_sub(a->obj.rolling_ball.pos, b->obj.rolling_ball.pos);
    phylib_coord v_rel = phylib_sub(a->obj.rolling_ball.vel, b->obj.rolling_ball.vel);
    phylib_coord n = phylibNor(r_ab);
    double v_rel_n = phylib_dot_product(v_rel, n);

    a->obj.rolling_ball.vel.x -= v_rel_n * n.x;
    a->obj.rolling_ball.vel.y -= v_rel_n * n.y;

    b->obj.rolling_ball.vel.x += v_rel_n * n.x;
    b->obj.rolling_ball.vel.y += v_rel_n * n.y;

    double firstSpeed = phylib_length(a->obj.rolling_ball.vel);
    double secondSpeed = phylib_length(b->obj.rolling_ball.vel);

    if (firstSpeed > PHYLIB_VEL_EPSILON)
    {
        a->obj.rolling_ball.acc.x = -a->obj.rolling_ball.vel.x / firstSpeed * PHYLIB_DRAG;
        a->obj.rolling_ball.acc.y = -a->obj.rolling_ball.vel.y / firstSpeed * PHYLIB_DRAG;
    }

    if (secondSpeed > PHYLIB_VEL_EPSILON)
    {
        b->obj.rolling_ball.acc.x = -b->obj.rolling_ball.vel.x / secondSpeed * PHYLIB_DRAG;
        b->obj.rolling_ball.acc.y = -b->obj.rolling_ball.vel.y / secondSpeed * PHYLIB_DRAG;
    }
}

void phylib_bounce(phylib_object **a, phylib_object **b)
{

    // Check if object a is PHYLIB_ROLLING_BALL
    if (*a == NULL || (*a)->type != PHYLIB_ROLLING_BALL)
    {
        return;
    }

    switch ((*b)->type)
    {

    // Case 1: b is a HCUSHION or VCUSHION
    case PHYLIB_HCUSHION:
    case PHYLIB_VCUSHION:
        handleCushionBounce(*a, *b);
        break;

    // Case 2: b is a HOLE - Free memory of a and set it to NULL
    case PHYLIB_HOLE:
        free(*a);
        *a = NULL;
        break;

    // Case 3: b is a STILL_BALL - Upgrade STILL_BALL to ROLLING_BALL and proceed to CASE 4
    case PHYLIB_STILL_BALL:
        (*b)->type = PHYLIB_ROLLING_BALL;
        (*b)->obj.rolling_ball.number = (*b)->obj.still_ball.number;
        (*b)->obj.rolling_ball.acc.x = 0.0;
        (*b)->obj.rolling_ball.acc.y = 0.0;
        (*b)->obj.rolling_ball.vel.x = 0.0;
        (*b)->obj.rolling_ball.vel.y = 0.0;
        (*b)->obj.rolling_ball.pos = (*b)->obj.still_ball.pos;

    // Case 4: b is a ROLLING_BALL - Handle the bounce
    case PHYLIB_ROLLING_BALL:
        handleRollingBallBounce(*a, *b);
        break;
    }
}

/* This function should return the number of ROLLING_BALLS on the table. */
unsigned char phylib_rolling(phylib_table *t)
{

    if (t == NULL)
    {
        return 0;
    }

    unsigned char rolling_count = 0;

    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        phylib_object *obj = t->object[i];
        if (obj != NULL && obj->type == PHYLIB_ROLLING_BALL)
        {
            rolling_count++;
        }
    }

    return rolling_count;
}

/* This function should return if there are no ROLLING_BALLs on the table, it should return NULL.
Otherwise, it should return a phylib_copy_table. */

phylib_table *phylib_segment(phylib_table *table)
{
    if (table == NULL || countRollingBalls(table) == 0)
    {
        return NULL;
    }

    return simulateTable(table);
}

// Helper function implementations
int countRollingBalls(phylib_table *table)
{
    return phylib_rolling(table);
}

phylib_table *copyAndRollBalls(phylib_table *table, phylib_table *resultTable, double currentTime)
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (resultTable->object[i] != NULL && resultTable->object[i]->type == PHYLIB_ROLLING_BALL)
        {
            phylib_roll(resultTable->object[i], table->object[i], currentTime);
        }
    }
    return resultTable;
}

phylib_table *checkBallStopped(phylib_table *resultTable)
{
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
    {
        if (resultTable->object[i] != NULL && resultTable->object[i]->type == PHYLIB_ROLLING_BALL && phylib_stopped(resultTable->object[i]))
        {
            return resultTable;
        }
    }
    return NULL;
}

phylib_table *checkCollisionAndBounce(phylib_table *resultTable, int i, int j)
{
    if (resultTable->object[i] != NULL && resultTable->object[i]->type == PHYLIB_ROLLING_BALL &&
        resultTable->object[j] != NULL && resultTable->object[i] != resultTable->object[j] &&
        phylib_distance(resultTable->object[i], resultTable->object[j]) < 0.0)
    {
        phylib_bounce(&resultTable->object[i], &resultTable->object[j]);
        return resultTable;
    }
    return NULL;
}

phylib_table *simulateTable(phylib_table *table)
{
    phylib_table *resultTable = phylib_copy_table(table);
    double currentTime = PHYLIB_SIM_RATE;

    while (currentTime <= PHYLIB_MAX_TIME)
    {
        resultTable = copyAndRollBalls(table, resultTable, currentTime);

        phylib_table *stoppedTable = checkBallStopped(resultTable);
        if (stoppedTable != NULL)
        {
            free(resultTable);
            return stoppedTable; // Stopping condition 1: Ball has stopped
        }

        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++)
        {
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++)
            {
                phylib_table *collisionTable = checkCollisionAndBounce(resultTable, i, j);
                if (collisionTable != NULL)
                {
                    free(resultTable);
                    return collisionTable; // Stopping condition 2: Collision detected and bounce applied
                }
            }
        }

        currentTime += PHYLIB_SIM_RATE;
        resultTable->time += PHYLIB_SIM_RATE; // Time update
    }

    free(resultTable);
    return NULL; // Max time reached
}
