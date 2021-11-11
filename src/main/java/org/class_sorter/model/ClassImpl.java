package org.class_sorter.model;

import java.util.ArrayList;
import java.util.List;

public class ClassImpl implements Class_ {
    private final String name;
    private int capacity;
    private List<Camper> enrolled_A;
    private List<Camper> enrolled_B;
    private List<Camper> enrolled_C;
    private List<Camper> enrolled_D;
    private List<Camper> firstPrefs;
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
        enrolled_A = new ArrayList<>();
        enrolled_B = new ArrayList<>();
        enrolled_C = new ArrayList<>();
        enrolled_D = new ArrayList<>();
        firstPrefs = new ArrayList<>();
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
    public int getNumEnrolled(int i) {
        if (! ( 0 < i && i < 5)) {
            throw new IllegalArgumentException("Must be 1-4 to align with classes");
        } else {
            if (i == 1) {
                return enrolled_A.size();
            } else if (i == 2) {
                return enrolled_B.size();
            } else if (i == 3) {
                return enrolled_C.size();
            } else {
                return enrolled_D.size();
            }
        }
    }

    @Override
    public boolean getRequiresShootingForm() {
        return requiresShootingForm;
    }

    @Override
    public List getFirstPrefs() {
        return firstPrefs;
    }

    @Override
    public void changeShootingForm(boolean v) {
        requiresShootingForm = v;
    }


    @Override
    public List<Camper> getCampersEnrolled(int i ) {
        if (! ( 0 < i && i < 5)) {
            throw new IllegalArgumentException("Must be 1-4 to align with classes");
        } else {
            if (i == 1) {
                return enrolled_A;
            } else if (i == 2) {
                return enrolled_B;
            } else if (i == 3) {
                return enrolled_C;
            } else {
                return enrolled_D;
            }
        }
    }

    @Override
    public int enrollCamper(Camper camper) {
        if (camper == null) {
            throw new IllegalArgumentException("Camper cannot be null");
        }
        if (camper.getClassA() != null && camper.getClassB() != null &&camper.getClassC() != null &&camper.getClassD() != null) {
            return 0;
        }
        if (isFull(1) && isFull(2) && isFull(3) && isFull(4)) {
            return 5;
        }
        if (camper.getClassA() == null && !isFull(1)) {
            camper.assignClassA(this);
            if (isFull(1) && isFull(2) && isFull(3) && isFull(4)) {
                return 5;
            }
            return 1;
        } else if (camper.getClassB() == null && !isFull(2)) {
            camper.assignClassB(this);
            if (isFull(1) && isFull(2) && isFull(3) && isFull(4)) {
                return 5;
            }
            return 2;
        } else if (camper.getClassC() == null && !isFull(3)) {
            camper.assignClassC(this);
            if (isFull(1) && isFull(2) && isFull(3) && isFull(4)) {
                return 5;
            }
            return 3;
        } else if (camper.getClassD() == null && !isFull(4)) {
            camper.assignClassD(this);
            if (isFull(1) && isFull(2) && isFull(3) && isFull(4)) {
                return 5;
            }
            return 4;
        } else {
            return 6;
        }
    }

    @Override
    public void removeCamper(Camper camper, int i) {
        if (! ( 0 < i && i < 5)) {
            throw new IllegalArgumentException("Must be 1-4 to align with classes");
        } else {
            if (i == 1) {
                if (camper == null) {
                    throw new IllegalArgumentException("Camper can't be null");
                }
                enrolled_A.remove(camper);
                camper.getClasses().remove(this);
            } else if (i == 2) {
                if (camper == null) {
                    throw new IllegalArgumentException("Camper can't be null");
                }
                enrolled_B.remove(camper);
                camper.getClasses().remove(this);
            } else if (i == 3) {
                if (camper == null) {
                    throw new IllegalArgumentException("Camper can't be null");
                }
                enrolled_C.remove(camper);
                camper.getClasses().remove(this);
            } else {
                if (camper == null) {
                    throw new IllegalArgumentException("Camper can't be null");
                }
                enrolled_D.remove(camper);
                camper.getClasses().remove(this);
            }
        }
    }

    @Override
    public boolean isFull(int i) {
        if (! ( 0 < i && i < 5)) {
            throw new IllegalArgumentException("Must be 1-4 to align with classes");
        } else {
            if (i == 1) {
                return capacity <= enrolled_A.size();
            } else if (i == 2) {
                return capacity <= enrolled_B.size();
            } else if (i == 3) {
                return capacity <= enrolled_C.size();
            } else {
                return capacity <= enrolled_D.size();
            }
        }
    }

    @Override
    public boolean isEnrolled(Camper camper) {
        if (camper == null) {
            throw new IllegalArgumentException("Camper cannot be null");
        }
        return camper.getClassA() == this ||
                camper.getClassB() == this ||
                camper.getClassC() == this ||
                camper.getClassD() == this;
    }
}
