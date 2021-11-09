package org.class_sorter.controller;

import org.class_sorter.model.Camper;
import org.class_sorter.model.Class_;
import org.class_sorter.model.Model;
import org.class_sorter.model.ModelObserver;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.List;

public class ControllerImpl implements Controller{
    private Model model;

    public ControllerImpl(Model model) {
        if (model == null) {
            throw new IllegalArgumentException();
        }
        this.model = model;
    }

    @Override
    public List<Camper> getCampers() {
        return model.getCampers();
    }

    @Override
    public List<Class_> getClasses() {
        return model.getClasses();
    }

    @Override
    public List<Camper> getSortedCampers() {
        return model.getSortedCampers();
    }

    @Override
    public void createCampers(File file) throws FileNotFoundException {
        model.createCampers(file);
    }

    @Override
    public void createClasses(File file) throws FileNotFoundException {
        model.createClasses(file);
    }

    @Override
    public void sortCampers() {
        model.sortCampers();
    }
}
