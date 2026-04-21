function [ y ] = circularshiftt(x,m,N )
%The output y is the circular shift of the input signal x by m samples
%modulo N. The input signal x must be of length <= N.

close all

if length(x)>N
    error('length of x must be <= N')
end
n=[0:N-1];
nshift=mod(n-m,N);
y=x(nshift+1);
stem(n,x,'filled');
hold on
stem(n,y,'filled','r');
hold off

end

