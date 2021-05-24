package org.class_sorter.model;

import java.util.ArrayList;
import java.util.List;

public class CamperImpl implements Camper{
    private String name;
    private String cabin;
    private int age;
    boolean canShoot;
    private List<Class_> prefs;
    private List<Class_> classes;

    public CamperImpl(String name, String cabin, int age, boolean canShoot, List<Class_> prefs) {
        if (name == null || cabin == null || age < 0) {
            throw new IllegalArgumentException();
        }
        this.name = name;
        this.cabin = cabin;
        this.age = age;
        this.canShoot = canShoot;
        if (prefs == null) {
            this.prefs = new ArrayList<>();
        }
        this.prefs = prefs;
        classes = new ArrayList<>();
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public String getCabin() {
        return cabin;
    }

    @Override
    public boolean canShoot() {
        return canShoot;
    }

    @Override
    public int getAge() {
        return age;
    }

    @Override
    public List<Class_> getPrefs() {
        ArrayList<Class_> list = ((ArrayList<Class_>) prefs);
        return (List<Class_>) list.clone();
    }

    @Override
    public void addPref(Class_ c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        prefs.add(c);
    }

    @Override
    public void removePref(Class_ c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        prefs.remove(c);
    }

    @Override
    public void setPrefs(List<Class_> prefs) {
        if (prefs == null) {
            throw new IllegalArgumentException();
        }
        this.prefs = prefs;
    }

    @Override
    public List<Class_> getClasses() {
        return classes;
    }

    @Override
    public void addClass(Class_ c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        classes.add(c);
    }

    @Override
    public void removeClass(Class_ c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        classes.remove(c);
    }
}
