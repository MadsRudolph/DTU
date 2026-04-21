% Alias frekvenser

t=0:0.01:15;

x1=cos(0.2*2*pi*t);
x2=cos(1.2*2*pi*t);

n=0:15;
xsamp=cos(0.2*2*pi*1*n);

plot(t,x1,'color','blue')
hold on
plot(t,x2,'color','red')
hold on
stem(n,xsamp,'filled','color','black')
