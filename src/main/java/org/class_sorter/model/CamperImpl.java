package org.class_sorter.model;

import java.util.ArrayList;
import java.util.List;

public class CamperImpl implements Camper {
    private String firstName;
    private String lastName;
    private String ageGroup;
    private String cabin;
    boolean canShoot;
    private List<String> prefs;
    private List<Class_> classes;
    private Class_ classA;
    private Class_ classB;
    private Class_ classC;
    private Class_ classD;


    public CamperImpl(String firstName,String lastName,String ageGroup, String cabin, boolean canShoot, List<String> prefs) {
        if (firstName == null || lastName == null ||  ageGroup == null || cabin == null) {
            throw new IllegalArgumentException();
        }
        this.firstName = firstName;
        this.lastName = lastName;
        this.ageGroup = ageGroup;
        this.cabin = cabin;
        this.canShoot = canShoot;
        if (prefs == null) {
            this.prefs = new ArrayList<>();
        }
        this.prefs = prefs;
        classes = new ArrayList<>();

    }

    @Override
    public String getFirstName() {
        return firstName;
    }

    @Override
    public String getLastName() {
        return lastName;
    }

    @Override
    public String getAgeGroup() {
        return ageGroup;
    }

    @Override
    public String getCabin() {
        return cabin;
    }

    @Override
    public boolean getCanShoot() {
        return canShoot;
    }

    @Override
    public List<String> getPrefs() {
        return prefs;
    }

    @Override
    public void addPref(String c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        prefs.add(c);
    }

    @Override
    public void removePref(String c) {
        if (c == null) {
            throw new IllegalArgumentException();
        }
        prefs.remove(c);
    }

    @Override
    public void setPrefs(List<String> prefs) {
        if (prefs == null) {
            throw new IllegalArgumentException();
        }
        this.prefs = prefs;
    }

    @Override
    public List<Class_> getClasses() {
        if (classes == null) {
            return new ArrayList<>();
        }
        if (classA != null) {
            classes.add(classA);
        }
        if (classB != null) {
            classes.add(classB);
        }
        if (classC != null) {
            classes.add(classC);
        }
        if (classD != null) {
            classes.add(classD);
        }
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

    @Override
    public Class_ getClassA() {
        return classA;
    }

    @Override
    public Class_ getClassB() {
        return classB;
    }

    @Override
    public Class_ getClassC() {
        return classC;
    }

    @Override
    public Class_ getClassD() {
        return classD;
    }

    @Override
    public void assignClassA(Class_ cl) {
        if (cl == null) {
            throw new IllegalArgumentException("Class cannot be null");
        }
        classA = cl;
        cl.getCampersEnrolled(1).add(this);
        addClass(cl);
    }

    @Override
    public void assignClassB(Class_ cl) {
        if (cl == null) {
            throw new IllegalArgumentException("Class cannot be null");
        }
            classB = cl;
            cl.getCampersEnrolled(2).add(this);
            addClass(cl);
    }

    @Override
    public void assignClassC(Class_ cl) {
        if (cl == null) {
            throw new IllegalArgumentException("Class cannot be null");
        }
            classC = cl;
            cl.getCampersEnrolled(3).add(this);
            addClass(cl);
    }

    @Override
    public void assignClassD(Class_ cl) {
        if (cl == null) {
            throw new IllegalArgumentException("Class cannot be null");
        }
            classD = cl;
            cl.getCampersEnrolled(4).add(this);
            addClass(cl);
    }
    @Override
    public void cleanPrefs(List<Class_> classesList) {
        List<String> availableClasses = new ArrayList<>();
        for (Class_ cl : classesList) {
            availableClasses.add(cl.getName());
        }
        if (prefs.size() != 0) {
            List<String> cleanPrefs = new ArrayList<>();
            cleanPrefs.add(prefs.get(0));
            for (String p : prefs) {
                boolean contained = false;
                for (int i = 0; i < cleanPrefs.size(); i++) {
                    if (p.equals(cleanPrefs.get(i))) {
                        contained = true;
                    }
                }
                if (!contained) {
                    cleanPrefs.add(p);
                    for (int j = 0; j < availableClasses.size(); j++) {
                        if (p.equals(availableClasses.get(j))) {
                            availableClasses.remove(j);
                            j = availableClasses.size();
                        }
                    }
                }
            }
            prefs = cleanPrefs;
        }
        while (prefs.size() < 6 && availableClasses.size() > 0) {
            int randomInt = (int)(Math.random() * availableClasses.size());
            prefs.add(availableClasses.get(randomInt));
            availableClasses.remove(randomInt);
        }
    }
}
