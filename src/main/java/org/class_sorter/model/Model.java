package org.class_sorter.model;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public interface Model {

    List<Camper> getCampers();

    List<Class_> getClasses();

    /**
     * retrieves a list of campers that have been sorted into classes. Their classes have been filled 1-4
     **/
    List<Camper> getSortedCampers();

    /**
     * instantiates a list of campers that represent the campers at camp.
     */
    void createCampers(File file) throws FileNotFoundException;

    /**
     * instantiates a list of classes that represent the active classes at camp
     * @param file
     */
    void createClasses(File file) throws FileNotFoundException;

    void addObserver(ModelObserver observer);

    /**
     * Removes an observer from the active observer list
     */
    void removeObserver(ModelObserver observer);

    /**
     * sorts campers into classes based on prefs
     */
    void sortCampers();


}
