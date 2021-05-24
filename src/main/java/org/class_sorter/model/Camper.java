package org.class_sorter.model;

import java.util.List;

public interface Camper {
    /** returns the name of the camper */
    String getName();

    /** returns the camper's cabin */
    String getCabin();

    /** returns whether or not the camper can do shooting sports */
    boolean canShoot();

    /** returns the age of the camper */
    int getAge();

    /** returns the preferences of the camper */
    List<Class_> getPrefs();

    /** adds a class to the preferences of the camper */
    void addPref(Class_ c);

    /** removes a class from the preferences of the camper */
    void removePref(Class_ c);

    /** sets the camper's preferences given a list of classes. */
    void setPrefs(List<Class_> prefs);

    /** returns the classes that the camper is already enrolled in */
    List<Class_> getClasses();

    /** adds a class to the list of classes the camper is enrolled in */
    void addClass(Class_ c);

    /** removes a class from the campers list of enrolled classes */
    void removeClass(Class_ c);
}
