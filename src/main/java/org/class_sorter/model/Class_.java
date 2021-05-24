package org.class_sorter.model;

import java.util.List;

public interface Class_ {
    /** Returns the name of the class */
    String getName();

    /** returns the maximum amount of campers that can get into the class */
    int getCapacity();

    /** returns the number of campers already enrolled in a class */
    int getNumEnrolled();

    /** returns whether or not the child can participate in shooting sports */
    boolean getRequiresShootingForm();

    /** changes whether or not a shooting form is required */
    void changeShootingForm(boolean v);

    /** returns the number of campers already enrolled in a class */
    List<Camper> getCampersEnrolled();

    /** modifies the maximum amount of campers that can get into the class */
    void changeCapacity(int n);

    /** enrolls a camper in the class */
    void enrollCamper(Camper camper);

    /** removes a camper from a class given the camper */
    void removeCamper(Camper camper);

    /** returns whether or not the class is full */
    boolean isFull();

    /** returns whether or not a camper is already enrolled in the class */
    boolean isEnrolled(Camper camper);
}
