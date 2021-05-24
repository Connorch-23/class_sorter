package org.class_sorter.model;

import java.util.ArrayList;
import java.util.List;

public class ClassImpl implements Class_ {
    private final String name;
    private int capacity;
    private List<Camper> enrolled;
    private boolean requiresShootingForm;

    public ClassImpl(String name, int capacity, boolean requiresShootingForm) {
        if (name == null) {
            throw new IllegalArgumentException("Name cannot be null");
        }
        if (capacity < 1) {
            throw new IllegalArgumentException("Capacity is too low");
        }
        this.name = name;
        this.capacity = capacity;
        enrolled = new ArrayList<>();
        this.requiresShootingForm = requiresShootingForm;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getCapacity() {
        return capacity;
    }

    @Override
    public int getNumEnrolled() {
        return enrolled.size();
    }

    @Override
    public boolean getRequiresShootingForm() {
        return requiresShootingForm;
    }

    @Override
    public void changeShootingForm(boolean v) {
        requiresShootingForm = v;
    }


    @Override
    public List<Camper> getCampersEnrolled() {
        ArrayList<Camper> list = ((ArrayList<Camper>) enrolled);
        return (List<Camper>) list.clone();
    }

    @Override
    public void changeCapacity(int n) {
        if (capacity < 1) {
            throw new IllegalArgumentException("Capacity is too low");
        }
        capacity = n;
    }

    @Override
    public void enrollCamper(Camper camper) {
        if (camper == null) {
            throw new IllegalArgumentException("Camper can't be null");
        }
        if (!isFull()) {
            if (!isEnrolled(camper)) {
                enrolled.add(camper);
            }
        }
    }

    @Override
    public void removeCamper(Camper camper) {
        if (camper == null) {
            throw new IllegalArgumentException("Camper can't be null");
        }
        enrolled.remove(camper);
    }

    @Override
    public boolean isFull() {
        return capacity == enrolled.size();
    }

    @Override
    public boolean isEnrolled(Camper camper) {
        if (enrolled.contains(camper)) {
            return true;
        } else {
            for (Camper c : enrolled) {
                if (c.getName().equals(camper.getName())) {
                    return true;
                }
            }
        }
        return false;
    }
}
