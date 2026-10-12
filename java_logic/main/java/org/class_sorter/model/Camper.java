package org.class_sorter.model;

import java.util.List;

public interface Camper {
    /**
     * returns the name of the camper
     */
    String getFirstName();

    /**
     * returns the last name of the camper
     */
    String getLastName();

    /**
     *returns age of the camper
     */
    int getAge();

    /**
     * returns the camper's cabin
     */
    String getCabin();

    /**
     * returns whether or not the camper can do shooting sports
     */
    boolean getCanShoot();

    /**
     * returns the preferences of the camper
     */
    List<String> getPrefs();

    /**
     * adds a class to the preferences of the camper
     */
    void addPref(String c);

    /**
     * removes a class from the preferences of the camper
     */
    void removePref(String c);

    /**
     * sets the camper's preferences given a list of classes.
     */
    void setPrefs(List<String> prefs);

    /**
     * returns the classes that the camper is already enrolled in
     */
    List<Class_> getClasses();

    /**
     * adds a class to the list of classes the camper is enrolled in
     */
    void addClass(Class_ c);

    /**
     * removes a class from the campers list of enrolled classes
     */
    void removeClass(Class_ c);

    /**
     * sets the available classes
     */
    /**
     * returns the camper's A class;
     * @return
     */
    Class_ getClassA();
    /**
     * returns the camper's B class;
     * @return
     */
    Class_ getClassB();
    /**
     * returns the camper's C class;
     * @return
     */
    Class_ getClassC();
    /**
     * returns the camper's D class;
     * @return
     */
    Class_ getClassD();

    /**
     * assigns the class;
     */
    void assignClassA(Class_ cl);
    /**
     * assigns the class;
     */
    void assignClassB(Class_ cl);
    /**
     * assigns the class;
     */
    void assignClassC(Class_ cl);
    /**
     * assigns the class;
     */
    void assignClassD(Class_ cl);

    /**
     * removes any duplicate preferences from a camper's list of preferred classes.
     * If camper does not have a full list of preferences, this method fills
     * them in with a randomly generated list.
     */
    void cleanPrefs(List<Class_> classesList);
}
