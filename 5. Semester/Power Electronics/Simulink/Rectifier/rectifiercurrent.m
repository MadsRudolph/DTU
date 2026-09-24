Vs=120;
f=50;
L=6.5e-3;
R=2.5;
E=10;
Z=sqrt(R^2+(2*pi*L*f)^2);
theta=atan(2*pi*L*f/R);
w=2*pi*f;
x=0;
ist=sqrt(2)*Vs/Z*(sin(w*x-theta)+2/(1-exp(-R/L*pi/w))*sin(theta)*exp(-R/L*x))-E/R;

io=@(x)sqrt(2)*Vs/Z*(sin(w*x-theta)+2/(1-exp(-R/L*pi/w))*sin(theta)*exp(-R/L*x))-E/R;
io2=@(x)(sqrt(2)*Vs/Z*(sin(w*x-theta)+2/(1-exp(-R/L*pi/w))*sin(theta)*exp(-R/L*x))-E/R).^2;
iave=integral(io,0,(1/f)/2)*f
irms2=integral(io2,0,(1/f)/2)*f
irms=sqrt(irms2)
