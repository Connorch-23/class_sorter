package org.class_sorter.controller;

import org.class_sorter.model.Camper;
import org.class_sorter.model.Class_;
import org.class_sorter.model.ModelObserver;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public interface Controller {
    List<Camper> getCampers();

    String getFileName();

    void setFileName(String name);

    boolean getIsProgramDone();

    void closeProgram();

    List<Class_> getClasses();

    /**
     * retrieves a list of campers that have been sorted into classes. Their classes have been filled 1-4
     **/
    List<Camper> getSortedCampers();

    /**
     * returns whether or not the list of campers has been sorted yet
     */
    boolean getIsSorted();

    /**
     * instantiates a list of campers that represent the campers at camp.
     */
    void createCampers(File file) throws FileNotFoundException;

    /**
     * instantiates a list of classes that represent the active classes at camp
     */
    void createClasses(File file) throws FileNotFoundException;


    /**
     * sorts campers into classes based on prefs
     */
    void sortCampers();
}
