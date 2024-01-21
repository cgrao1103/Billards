#include "phylib.h"
#include <stdlib.h>
#include <string.h>

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
    if(newTable == NULL){
        return NULL;
    }
    newTable->time=0.0;
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
    } else {
        *dest = (phylib_object *)malloc(sizeof(phylib_object));
        if (*dest != NULL) {
            memcpy(*dest, *src, sizeof(phylib_object));
        }
    }
}

phylib_table *phylib_copy_table( phylib_table *table ){
    if (table == NULL) {
        return NULL;
    }
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    if(newTable == NULL){
        newTable->time = table->time;
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
            phylib_copy_object(&(newTable->object[i]), &(table->object[i]));
        }
    }
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        free(table->object[i]);
    }

    free(table);
    return newTable;

}

void phylib_add_object( phylib_table *table, phylib_object *object ){
    if (table == NULL || object == NULL) {
    }
        
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] == NULL) {
            table->object[i] = object;
            break;
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
