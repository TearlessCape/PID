package simulation;

public class Pole {
    
    public final static double
        DEG360 = Math.PI * 2,
        DEG90 = Math.PI / 2,
        GRAVITY = 9.81;
        
    public final double
        LENGTH,
        MASS,
        INERTIA;

    private double
        elapsed = 0,
        angle = 0,
        angleVelocity = 0,
        anglePIDAcceleration = 0,
        angleExternalAcceleration = 0;

    public Pole() {

        LENGTH = 1;
        MASS = 10;
        INERTIA = MASS * LENGTH * LENGTH;

    }
    
    public Pole(double length, double mass) {

        LENGTH = length;
        MASS = mass;
        INERTIA = MASS * LENGTH * LENGTH;

    }

    private boolean done = false;
    
    public boolean getDone() {return done;}

    public double getElapsed() {return elapsed;}
    public double getAngle() {return angle;}
    public double getAngleVelocity() {return angleVelocity;}
    public double getProcessVariable() {return getAngle();}
    
    public void setPIDTorque(double torque) {anglePIDAcceleration = torque / INERTIA;}
    public void setExternalTorque(double torque) {angleExternalAcceleration = torque / INERTIA;}
    
    public void update(double dTime, int repeats) {
        
        for (int i = 0; i < repeats; i++) {
            
            double stepAngleAcceleration = anglePIDAcceleration + angleExternalAcceleration;
            stepAngleAcceleration -= GRAVITY / LENGTH * Math.sin(DEG360 - angle);
            angleVelocity += stepAngleAcceleration * dTime / repeats;
            angle += angleVelocity * dTime / repeats;
        
        }
        
        elapsed += dTime;
        done = Math.abs(angle) > DEG90;
    
    }
    
}