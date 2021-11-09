package org.class_sorter.model;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.List;

public class ModelImpl implements Model {
    ArrayList<Camper> campers;
    ArrayList<Class_> classes;
    List<ModelObserver> observers;
    boolean areCampersSorted;

    public ModelImpl() {
        campers = new ArrayList<>();
        classes = new ArrayList<>();
        observers = new ArrayList<>();
        areCampersSorted = false;
    }


    @Override
    public List<Camper> getCampers() {
        return campers;
    }

    @Override
    public List<Class_> getClasses() {
        return classes;
    }

    @Override
    public List<Camper> getSortedCampers() {
        if (!areCampersSorted) {
            sortCampers();
        }
        return campers;
    }

    @Override
    public void createCampers(File file) throws FileNotFoundException {
        campers = (ArrayList<Camper>) Factory.createCampers(file);
    }

    @Override
    public void createClasses(File file) throws FileNotFoundException {
        classes = (ArrayList<Class_>) Factory.createClasses(file);
    }

    @Override
    public void addObserver(ModelObserver observer) {
        observers.add(observer);
    }

    @Override
    public void removeObserver(ModelObserver observer) {
        observers.remove(observer);
    }

    @Override
    public void sortCampers() {
        ArrayList<Camper> rawCampers = (ArrayList<Camper>) campers.clone();
        ArrayList<Class_> availableClasses = (ArrayList<Class_>) classes.clone();
        int counter = 0;
        while (rawCampers.size() != 0 || availableClasses.size() != 0 || counter != 500) {
            if (counter == 499) {
                int hello = 0;
                //do something
            }
            for (int i = 0; i < rawCampers.size(); i++) {
                Camper camper = rawCampers.get(i);
                for (int j = 0; j < availableClasses.size(); j++) {
                    Class_ cl = availableClasses.get(j);
                    if (camper.getPrefs().size() == 0) {
                        if (camper.getClassA() == null || camper.getClassB() == null || camper.getClassC() == null || camper.getClassD() == null) {
                            camper.cleanPrefs(availableClasses);
                            j = 0;
                        } else {
                            rawCampers.remove(i);
                            j = availableClasses.size();
                        }
                    } else if (cl.getName().equals(camper.getPrefs().get(0))) {
                        int enrollCamper = cl.enrollCamper(camper);
                        if (enrollCamper == 0) {
                            rawCampers.remove(camper);
                            i--;
                            j = availableClasses.size();
                        }
                        if (enrollCamper == 5) {
                            availableClasses.remove(cl);
                            j--;
                            }
                        if (enrollCamper > 0 && enrollCamper < 5) {
                            j = availableClasses.size();
                        }
                        camper.getPrefs().remove(0);
                    }
                }
            }
            counter++;
        }






        /*
        for (int i = 0; i < 4; i++) {
            for (Camper camper : campers) {

                int classSize = camper.getClasses().size();
                while (classSize == camper.getClasses().size() && camper.getPrefs().size() > 0) {
                    for (Class_ cl : classes) {
                        if (camper.getPrefs().size() > 0) {
                            if (cl.getName().equals(camper.getPrefs().get(0))) {
                                if (!cl.isEnrolled(camper)) {
                                    if (!cl.isFull(1) && camper.getClassA() == null) {
                                        camper.assignClassA(cl);
                                    } else if (!cl.isFull(2) && camper.getClassB() == null) {
                                        camper.assignClassB(cl);
                                    } else if (!cl.isFull(3) && camper.getClassC() == null) {
                                        camper.assignClassC(cl);
                                    } else if (!cl.isFull(4) && camper.getClassD() == null) {
                                        camper.assignClassD(cl);
                                    }
                                }
                            }
                        }
                    }
                    camper.getPrefs().remove(0);
                }
            }
        }





        for (int i = 0; i < 4; i++) {
            for (Camper camper : campers) {
                int classSize = camper.getClasses().size();
                for (int j = 0; j < classes.size(); j++) {
                    Class_ cl = classes.get(j);
                    if (camper.getPrefs().size() > 0) {
                        if (camper.getPrefs().get(0).equals(cl.getName())) {
                            if (!cl.isEnrolled(camper)) {
                                if (!cl.isFull(1)) {
                                    camper.assignClassA(cl);
                                    j = classes.size();
                                } else if (!cl.isFull(2)) {
                                    camper.assignClassB(cl);
                                    j = classes.size();
                                } else if (!cl.isFull(3)) {
                                    camper.assignClassC(cl);
                                    j = classes.size();
                                } else if (!cl.isFull(4)) {
                                    camper.assignClassD(cl);
                                    j = classes.size();
                                }
                                   //means the class is entirely full
                            }
                            if (!cl.isEnrolled(camper)) {
                                j = 0;
                            } else {
                                if (classSize != camper.getClasses().size()) {
                                    j = classes.size();
                                } else {
                                    j = 0;
                                }
                            }
                            camper.getPrefs().remove(0);
                            //means the camper is enrolled in this class or whats above
                        }
                        //means the preference does not match the class or whats above
                        // end of classes loop
                    }
                }
                //end of camper loop, new camper after this
            }
        }
    */
    }
}
