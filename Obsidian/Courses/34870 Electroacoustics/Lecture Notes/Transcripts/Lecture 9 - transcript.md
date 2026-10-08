---
course: "34870"
type: transcript
lecture: 9
source: "Slides/34870_Lecture_9_E26_and_Loudspeaker_Project.mp4"
---
# Lecture 9 — transcript of the commented slides

> [!info] Machine transcript
> Whisper large-v3 (faster-whisper, GPU), English forced, vocabulary prompt. VCH speaks with a strong accent, so expect slips such as "battlefield" = Butterworth, "Link with Rayleigh" = Linkwitz-Riley, "Sobel" = Zobel, "buffer" = woofer, "pistol" = piston, "Tillis-Moll" = Thiele-Small, "Mazda to LTSpice" = Matlab2LTspice. Timestamps are mm:ss into the video. The note built from it: [[Lecture 9 - Loudspeaker Systems & Crossovers]].

[00:05] Welcome to the presentation on loudspeaker systems and loudspeaker projects. This is the last presentation on loudspeakers.  
[00:13] Today we will talk about crossovers, mainly passive crossovers, also active crossovers and all the issues associated with them.  
[00:27] In the end we will introduce the loudspeaker project that you have to do in the lab.  
[00:35] The passive crossover filters, you have an example shown here, are passive circuits.  
[00:40] work on the amplifier signal so they are placed after the audio amplifier. They can be placed  
[00:46] inside the box, they are quite convenient because of that, so the box only needs one connection to  
[00:51] the audio amplifier. A single amplifier is sufficient to feed a box in this way, but they  
[01:04] have their throwbacks. As we will see, the passive crossovers affect the performance of the drivers.  
[01:10] If you fit passive crossovers you need to test the system and with listening test as well.  
[01:21] Active crossovers. Active crossovers are less common, they need more hardware. The filtering  
[01:29] is done on the non-amplified signal before the amplifier. Therefore you need as many  
[01:35] amplified channels as units you have with active filter. This means you need an active box or you  
[01:46] need extra hardware outside the box in order to implement this kind of filters.  
[01:51] They are implemented digitally in digital signal processors and the design is software made.  
[02:00] There are many other things one can do with active filters, active crossovers, not only crossovers,  
[02:07] but also shaping the signal, tuning the box in different ways. All this has to be done before  
[02:12] amplification. In this case, as in the passive case, you also need to test the box with subjective tests.  
[02:23] Why do you need crossovers? A single unit is not generally sufficient to cover  
[02:30] with high quality the whole audio range, so normally the solution is having several units  
[02:36] in a box to cover the range with units specialized on different ranges.  
[02:40] In this example we have a unit, a mid or woofer unit that covers from low frequencies to mid frequencies and a tweeter unit that covers high frequencies.  
[02:50] So the problem comes that there is an overlap region where you have to cross over the units.  
[02:56] If you just put together the units then they will mix probably in a not nice way. You need to organize this mixing.  
[03:03] mixing. This example, I cannot play it here, but you have an audio signal that covers the whole  
[03:18] audio range. This can be filtered as a low-pass filter and get a low-pass signal version  
[03:27] of the original signal that goes to the mid unit. And then at the same time a high-pass filter  
[03:34] we'll create a high pass version that will go to the tweeter unit. It's also possible to create  
[03:41] bandpass filters for mid units by combining two of these. Let's have a review of possible filters  
[03:52] in order of complexity. These are the filters you might use in your project.  
[03:59] Crossover filters are not very complicated, they are simple electrical filters. The first advice  
[04:06] is make it as simple as possible, but considering all the effects of the filter. This is the simplest  
[04:14] filter possible. It's just a coil for low pass, and as the coil has an impedance that grows with  
[04:22] frequency, this is a low pass filter. It has a decay of 20 dB per decade, and the transfer function  
[04:32] is very easy to deduce from the circuit, as you can see here, and it's also possible to obtain  
[04:37] the value of the component, the L, from the desired crossover frequency, cutoff frequency.  
[04:48] You have to remember here that we are modeling the unit as a resistor, and this is far from  
[04:53] reality. If you remember from your exercises and from previous teaching, the input impedance of  
[04:59] a unit is not a resistor but it's a complicated function that has a mechanical resonance a coil  
[05:06] behavior and so on so keep this in mind we will talk about this later this is the high pass  
[05:15] counterpart of the low pass first order filter in this case we have a capacitor the capacitor  
[05:21] has an impedance that increases with frequency allowing more signal high frequency as you can  
[05:27] see here the calculation of the components is also very easy by analyzing this circuit  
[05:36] Here you have a simple example of calculation of first-order filters for a given crossover  
[05:43] frequency, which is the same for the high-pass, low-pass. It doesn't have to be. You may choose  
[05:48] different crossover frequencies that would be something that might help you shaping the  
[05:53] response. And this is the result in this case. Another filter with two components is the second  
[06:02] order ideal low-pass Butterworth filter. This filter has doubled the slope as the first order.  
[06:11] If one decides for a Q of 1 over square root of 2, which is the best choice, to have a drop of this  
[06:17] value at the crossover frequency, then it's also possible to reduce the transfer function and the  
[06:24] values of the components like this. The phase change here is doubled as the first order. As  
[06:33] you can see is pi. Very similarly the high pass counterpart has the components swapped c and l  
[06:44] and the slope is the same and the phase change is the same but in the other direction  
[06:49] and the reduction of the components is similar by considering a q of 1 over square root of 2.  
[06:58] It's possible to define high order filters but I think it's less advisable using  
[07:03] very high order filters if you can avoid it. The more the components, the more problems you can  
[07:11] have in the end. One of the problems, we will repeat this advice later, is that you cannot  
[07:18] choose exact values of the components, you only can choose normalized values. So you always have  
[07:24] to settle for a normalized value that might not be exactly the same that you define here. This  
[07:31] This third-order Butterworth filter has also two versions, high-pass and low-pass.  
[07:36] And by choosing Q1 over square root of 2, we have the values of the components here.  
[07:41] Remember, we are defining a resistance as the input impedance of the unit, which is  
[07:49] not true.  
[07:50] A particular case that has been proposed for filter is a special kind of second-order filter,  
[08:02] which is constructed by putting together two first-order Butterworth filters, as explained  
[08:08] before.  
[08:09] If you do this, the resultant filter doesn't have a Q of 1 over square root of 2, but it has some interesting properties.  
[08:18] And these properties are that you can have a flat response when you combine two of these filters if you impair the polarity of one of the units.  
[08:29] This is part of your exercise today, and you can try and see.  
[08:32] And you can also look at the solutions to see how this is demonstrated.  
[08:36] They also have a decay of 40 dB per decade, and there are low-pass and high-pass versions.  
[08:44] We also designed a four-folder version of the Link with Rayleigh filter by cascading  
[08:55] or combining two second-order Butterworth filters like this.  
[09:01] These are the circuits and values of the components for this option.  
[09:09] In this case, you also obtain a flat response, and there's no need of swapping the terminals  
[09:14] of one of the units.  
[09:17] These filters, link-U-Reilly filters, are in the problems today, so you can look at  
[09:24] the solutions of the exercises to get some more theory about this.  
[09:35] Let's see what happens with the phase when you combine filters with the example of first-order  
[09:39] filters.  
[09:42] When you look at the crossover frequency, first order filters introduce 45 degrees at the  
[09:49] crossover frequency in advance or in delay, depending if it's high pass or low pass,  
[09:55] so you have a phase change in the end of 90 at the crossover frequency. For this kind of filter,  
[10:04] when you sum, and you can check this here, these two filters of first order, then you get a flat  
[10:10] response. The response is one together. Of course assuming you have a resistor as load and all the  
[10:18] different assumptions we have. If you combine second order filters then the combined phase  
[10:29] change is 180. And in this case you don't have a combined response of one. If you combine by  
[10:37] summing or through structing you can get a bump of 3 dB or a dip at the crossover frequency because  
[10:47] they don't sum in the same way as the first order. Bandpass filters. A bandpass filter can be done  
[11:00] by combining a low pass and high pass filter. The condition is that these two filters shouldn't  
[11:06] interact with each other so their crossover frequencies should be far apart from each other.  
[11:13] This is normally the case if you want a mid unit that is filtered for a tweeter and a woofer,  
[11:19] then those frequencies should be far apart. This is the moment for problem one and we  
[11:30] continue the lecture. In this part of the lecture we will see some issues that happen when you  
[11:37] place your passive filter in a real system. The first problem is the driver's response.  
[11:44] They have responses of magnitude and phase, and you have to look at this magnitude and phase at the crossover region, where you have to mix the two units.  
[11:57] So this phase difference and level difference at the crossover region add to the filter, so you have to consider them when designing the filter.  
[12:08] You have to adapt the filters to the driver's response.  
[12:12] Another issue is driver impedance. We have been assuming an resistor as driver impedance. This is not true.  
[12:23] The impedance has a shape like this. You have the original impedance which is provoked by the mechanical resonance  
[12:32] and you also have the coil behavior with an impedance that grows with frequency.  
[12:36] So depending on where your crossover frequency is in this frequency range, you will have different behaviors.  
[12:45] You have to check what happens at the input of the unit after the filter in order to see what  
[12:50] the effect of the load of the unit is on the filter. Another effect that you have to consider  
[12:59] is the effect of the box. The box is not an infinite baffle. It has edges. You have seen  
[13:05] in the previous lecture that the finite baffle provokes an effect and it can be quite a drastic  
[13:13] effect. So how you design the box, where you place the unit on the box is important. You have to try  
[13:20] and see or even do simulations in order to see the effect. Also the relative position between  
[13:28] the units you want to cross over. Another issue is directivity. Any loudspeaker, you can see that  
[13:36] in the example of the pistol in the buffer, has a directivity that cross with frequency.  
[13:41] This you have to consider when mixing, but you cannot avoid it, but you can mitigate it with some clever design.  
[13:49] But this is a physical fact that you have.  
[13:51] And finally, every driver has a different sensitivity.  
[13:56] This means that when you mix the units, they might have different sensitivities.  
[14:00] You might have to dump one of the units in order to make them even in the common response.  
[14:08] This is easy in a digital crossover because they have different amplifier channels, you can tune the amplification differently.  
[14:16] But in passive crossovers you need to introduce a special network that is called LPAD, we will talk about it later.  
[14:23] Here we explain how to match sensitivities in passive filters.  
[14:31] The way to reduce one of the unit's sensitivity is by using a pair of resistors, it's called LPAD.  
[14:40] And this is the calculation for a resistive load on what values to choose here.  
[14:47] Of course, this has an influence on the unit, and especially for buffers, this can spoil the low-frequency alignment of the buffer.  
[14:58] So try to avoid this kind of LPAD sensitivity adjustment for buffers.  
[15:04] Here are some examples.  
[15:10] This is a mid and a tweeter unit. As you can see, they have different levels, and we want to mix them, so we have to see that there is a phase difference, this is the phases, and these are the magnitudes.  
[15:24] The tweeter is the red one, the mid is the blue one. So you can see that there is a phase difference of approximately 180, let's say, depending on where you choose the crossover frequency to be.  
[15:42] So let's say we choose second-order battlefield filters. These are the characteristics of these  
[15:46] filters in an ideal setting. So we choose a crossover here for kilohertz. These filters  
[15:57] have a phase difference of 180, as we will show. So that seems to fit the phase difference  
[16:05] we observe in the total function of the units. So this is the result of the every unit  
[16:12] independently after filtering. As you can see here, they have the same phase because  
[16:19] minus pi is the same as plus pi, so the result is promising, but we will see the mixed result  
[16:27] in the next slide. This is the result of the output of the loudspeaker box, the pressure  
[16:36] at the distance. So in the brown plot you have the result of mixing with the same polarity in  
[16:43] in both units, and in the green one you have the result of inverting one of the units by  
[16:48] swapping the terminals. When you don't invert, you see that the phase is more or less fixed,  
[16:55] but in the case when you invert polarity, the phase changes a lot around the crossover  
[17:01] frequency. As to the magnitude, you either have a bump around the crossover frequency or a dip.  
[17:10] So, the problem is not solved, even though the filters seem to be the right solution.  
[17:17] You would need to do something else, because a solution would be moving the crossover frequency  
[17:24] or having different crossover frequencies for low pass and high pass.  
[17:29] I will leave that as an exercise in your project, it won't be a solution in this case, it's  
[17:35] just a matter of showing the problem.  
[17:39] One of the reasons of the problems could be that the filters are not having an ideal load.  
[17:45] If you have an ideal load, this is how they look like.  
[17:48] We showed this in the previous slide.  
[17:51] But when you look at the filters with the true load, with the driver load, they look  
[18:01] like this.  
[18:02] It's not the same as we had before.  
[18:04] Always check this.  
[18:10] Another example of the load of the unit on the filters.  
[18:14] In this case, we have a voice coil and we are in the region where the voice coil inductance  
[18:21] is high.  
[18:23] So if we have a first-order low-pass filter, which is a coil, then the driver coil adds  
[18:30] to the filter and completely spoils the response of the filter, as you can see here.  
[18:37] Yet another example.  
[18:38] In this example, we have chosen the crossover frequency for a high pass filter on the mechanical resonance of the input impedance of the unit.  
[18:49] This is the effect. We have a peak around the crossover frequency that we didn't want to have, but it happens because we are choosing the crossover at the resonance frequency.  
[19:02] The solution would be to move the crossover frequency to another frequency.  
[19:07] The solution of the problem of the electrical input impedance of the unit is the so-called Sobel network.  
[19:16] The Sobel network has two parts. One part is meant to compensate for the inductance effect and the other part is meant to compensate for the mechanical resonance of the unit.  
[19:30] However, this is a solution that has drawbacks, and we don't recommend it, and you are not allowed to use it in your project.  
[19:41] The problems are that it's very sensitive to the values of the components, so you could do more harm than good, and you will need values that are not standard, and they will be expensive.  
[19:54] Here we insist again on how to choose a filter depending on the responses of the units.  
[20:05] If we look at the phase response of the two units, you have to look at the crossover frequency you want to use.  
[20:13] Then you will see there is a difference. In this case, it's a 210 degrees difference.  
[20:19] So you have to choose among all the possible filters something that would preach this phase difference somehow.  
[20:30] You also have the choice of swapping the terminals of one of the units that introduces a 180 shift.  
[20:38] You can combine this with different filters in order to get a proper phase correction.  
[20:47] So, as a summary, when you run your speaker project, you can use a fast approach where you choose the units, decide the crossover frequency, find a filter, you build everything together and measure.  
[21:08] This is not a good approach because you will have different issues. You have to look at these issues.  
[21:14] So, use a more detailed and realistic approach where you measure your driver impedance and  
[21:24] response and you consider it together with the filters in an LTSpice design, and then  
[21:31] you play with this LTSpice design experiment, find out what are the issues, and then only  
[21:39] after being satisfied with this simulation you build the filter.  
[21:44] Finally you measure the response and maybe repeat the process if needed. Moreover you have to listen  
[21:52] to the speaker box and maybe this listening test will bring you to another repetition.  
[22:00] So there's no way around all this process. You need to check your designs, you need to experiment  
[22:05] as much as possible before you build and this is the only way to success. So after some more  
[22:15] problems, especially problem three is a design of crossovers using LTSpice LAMP models. Try this  
[22:24] as an exercise, it's interesting training. So, in this final part of the lecture we will talk  
[22:34] a bit about the project, loudspeaker project you have to do. You also have a loudspeaker project  
[22:40] guide in the corresponding contents module. In these slides we revisit, this slide is from  
[22:49] previous lecture, that was the last one, and this is about measuring the near or the far field.  
[22:54] We will recall this and then we will see how you implement this in LTSpice. Remember that the near  
[23:01] field pressure can be calculated in the circuit as the volume velocity through the radiation  
[23:06] impedance. That will be current in the impedance analogy. This is the radiation impedance,  
[23:10] low frequencies can be represented as a mass, so you get this. This is the expression for the  
[23:17] for the radiation impedance mass of a pistol on a baffle. In the far field then you can  
[23:27] model the the loudspeaker as a point source on an infinite plane and as such you get this  
[23:36] expression. So you use the volume velocity through the radiation impedance and then project it to the  
[23:43] far field using the point source expression. The thing is that if you relate the two expressions  
[23:49] then you get an expression, a formula which is only dependent on the distance and the piston  
[23:54] radius. So there is a response at far field and near field that is the same but with different  
[24:02] levels that allows measuring in the near field and getting far field responses.  
[24:10] How do you calculate or measure those three small parameters?  
[24:15] So you measure the input electrical impedance using a circuit of this kind  
[24:22] and the circuit consists of the loudspeaker that is excited by a source and then in between we put  
[24:29] a resistor. The function of the resistor is sampling the electrical current through it.  
[24:35] Its voltage will be proportional to the current using Ohm's law. So if we measure this voltage  
[24:40] and this voltage then we can get voltage and current with the proper operations and get  
[24:46] impedance. However, in the practical sense there would be a ground here and we cannot measure  
[24:53] directly this voltage with the equipment because it won't be grounded. So what we measure is this  
[24:57] voltage over the amplifier and the voltage on the unit, and then by some operation we get this  
[25:03] voltage over the resistor and therefore the input impedance. So the first parameter we get here is  
[25:12] the resonance frequency, f0, that's the frequency at which we have the maximum. We can also easily  
[25:17] get the maximum impedance here, and we can also get the resistance at dc that you can also measure  
[25:24] with a ohmmeter with a multimeter applied to the terminals without any excitation.  
[25:31] So from the expression of the input electrical impedance you can get the value of the maximum  
[25:41] impedance. So the impedance at which you have this F1 and F2 which are half power bandwidth  
[25:50] can be obtained like this, with RE and Z-marks, which are values that you have. So if you find  
[25:58] this impedance and find where they cut the curve, then you can get F1 and F2. And from F1 and F2,  
[26:05] and this value, then you can get the Qs, the total Q, electrical, and, no, total Q here,  
[26:13] electrical and mechanical Q. So this occurs for all three small parameters except for one,  
[26:20] that we have explained here. That's the next slide. The missing parameter is the compliance  
[26:29] of the suspension or equivalent volume. And there is a method to measure that. You have to change  
[26:36] something in the system in order to get the change in resonance frequency. One thing you can change  
[26:41] is the total mass. So if you add some extra mass to the diaphragm, this is a kind of material that,  
[26:49] moldable material that is attached to the diaphragm, that increases the mass and therefore  
[26:54] the resonance frequency changes from this change in resonance frequency you can deduce it you can  
[26:59] get the parameters so it's possible to get the parameters this way mms first and then from that  
[27:07] you can get all the parameters another way to do this if you don't want to do this mass change  
[27:12] is changing the other element here that's the compliance and the compliance you can change  
[27:18] by installing the unit on a closed box where you know the volume, for example.  
[27:24] This is actually what you will be doing in Lab D.  
[27:31] At this point, we revisit the measurement of the Tillis-Moll parameters  
[27:34] that we mentioned in the previous lecture.  
[27:37] In this case, we will redo the calculation of the VAS,  
[27:41] which is related to the compliance of the suspension,  
[27:45] by using, this time, a closed box.  
[27:47] The idea is measuring without the closed box and measuring with the box, which means that we will have the box parameters added.  
[27:59] That means that instead of having the suspension compliance, we have also the box compliance, which can be calculated from the volume of a box.  
[28:12] and this we can measure physically. At this point it is very useful to make the assumption that the mass at the back of the diaphragm  
[28:22] is the same as the mass at the front of the diaphragm, which is the radiation impedance reduced to only a mass.  
[28:29] This is not only convenient for the calculation, but it's probably less subject to uncertainties,  
[28:35] because if you don't do this, you can still calculate VAS,  
[28:39] but it would be subject to the asymptotic parameters that you need for this calculation.  
[28:48] Then you can also obtain alpha, the box ratio, from the relation of the frequency with closed  
[28:55] box and with infinite buffer. This can be possible because also the assumption we made here.  
[29:03] We also know that alpha is the ratio of box and suspension compliances, and from this and this  
[29:09] we can obtain Cs, the compliance of the suspension. And from that, we can obtain,  
[29:16] by multiplying by rho C square, the Vs, the parameter we were looking for.  
[29:22] Here we will summarize what you have to do in the project. So in your project, in this course,  
[29:28] you have to design a box that is actually formed by two boxes, a buffer box and a Twitter mid-range  
[29:35] box. So you start with an active filter and this active filter will make up the  
[29:46] crossover between buffer and mid-range. And then to that you add a passive crossover,  
[29:53] that will be the crossover between mid-range and tweeter. You will use now the amplifiers,  
[29:58] the same amplifier you have been using in regular exercises is a stereo amplifier so we will use the  
[30:04] two channels of the stereo amplifier. And these two channels will go into the chamber or listening  
[30:12] room and then you will have your boxes and your passive crossover. And the final part of the  
[30:18] design is designing the low frequency response. You don't have a lot of freedom here, you can  
[30:24] choose between several vents, several tubes you have for your box. You might be able to change  
[30:31] the volume by adding or removing a dumping material, maybe you could introduce an object  
[30:41] to reduce the volume, but you have to use the box you have for the project.  
[30:45] With this, the low frequency design won't be one of the alignments in the book, but you still can  
[30:52] calculate the lamp model and present your simulation in lamp model with lamp components  
[31:00] for the low frequency. The active crossover you will use is this product. It's called MiniDSP,  
[31:10] the company that produces it, and it's implemented in this box. It's controlled from the computer  
[31:17] through a USB connection and there is a user interface where you can decide  
[31:22] what to connect to what. The filter has two inputs and four outputs. You only use  
[31:28] one input and two outputs. So you have to connect it like this. You can decide the gains and the  
[31:35] gain of the input. And then if you go to outputs here then you get the possibility of defining  
[31:42] crossovers. There's also the possibility of finding some other things like big filters,  
[31:49] compression or other filters, but you have to bypass all these other possibilities in this  
[31:53] project and only use the crossover feature for channels 1 and 2. You have to choose the advanced  
[32:02] version. The MiniDSP has the possibility of basic definition of filters, but in order to have this  
[32:10] in LTSpice you need to define your own coefficients. So you have to click on advance and then you will  
[32:16] remove the coefficients here, the contents of this window here, and paste the coefficients you will  
[32:21] design for this filter. The procedure for designing the crossover filters in this project  
[32:29] looks like this. First thing is taking the measurements from lab D and E of the driver  
[32:38] input electrical impedance and the pressure response and then for this pressure response,  
[32:44] not for the impedance, you unwrap the face and compensate for distance and delay of the  
[32:51] measurement system. Then you choose the filters that you think could be okay looking at the phase  
[33:00] and response. We will provide a LTSpy circuit that you can use to construct your own version  
[33:11] of the measurement with filters and then you can import your results, your measurements.  
[33:16] you need to iterate this as many times as needed in order to get the okay response and only when  
[33:25] you are totally sure about this result you build actually the passive filter with components that  
[33:31] we will provide after that you test the system in a listening room it's a facility you haven't seen  
[33:39] yet but it's according to standards and it's meant for no speaker listen after that you might even  
[33:46] need to go back to point one and redesign the filters. Let's talk a bit about this  
[33:58] unwrapping and distance compensation. Why do you need this? First of all, the phases are presented  
[34:07] in MATLAB as wrapped phases, so they are shown in between plus and minus pi intervals, so you see  
[34:16] something here that is not very easy to deal with. So the first thing would be  
[34:21] unwrapping this and the other problem is that when you measure at a distance from a unit  
[34:26] there is a term, a term, remember this from the pressure from a point source  
[34:35] that you use to obtain the far-field pressure, there is this term and this term introduces  
[34:39] a huge phase lag as the frequency grows. So let's observe this in more detail. If you move this  
[34:47] into a larger phase variation, you see here the minus pi pi interval, you can unwrap it.  
[34:57] There is an unwrap function in MATLAB, but it's implemented in the files we are providing you with.  
[35:02] If you unbrap, then you get the unbrap phase, but due to the distance effect, you have a  
[35:09] huge lagging phase.  
[35:11] In this example, these are synthetic responses I'm using here, you have 39 pi, that's a lot.  
[35:20] So, the solution to this is removing this distance effect.  
[35:25] How?  
[35:25] Well, you remove this A minus JKR term by dividing by it, and then you get a phase that  
[35:33] is not moving so much. You have to do this for all units, but you have to do it in the same way,  
[35:40] so you have to do the same term for all units, the same distance compensation for all units.  
[35:46] Why is that? Well, the distances to different units, when you listen to them,  
[35:51] or you have a microphone here, will be slightly different, and that provokes phase differences  
[35:58] together with the responses of the units and also the filters if you have. But in order to preserve  
[36:05] this phase difference you need to compensate the same on all units. So this compensation  
[36:12] term should be the same for all units. So use the same distance compensation for all units.  
[36:24] Always R1 for all of them. In some cases it will be too short, some others it will be too big,  
[36:30] but always use the same so you preserve this phase difference between units.  
[36:34] In the end you will end up with phase responses like this. This is my synthetic case. So maybe  
[36:40] you will hit the perfect compensation for one unit but not for the other units. But that's what you  
[36:46] want because you want to see the phase differences between units. So this is what I would expect you  
[36:55] obtain in order to see phase differences. You will be looking at the crossover frequencies in this  
[37:01] graph. Then another issue, how do you implement, I've been talking about implementing input  
[37:11] impedance and transfer function of the unit in LTSpice. This you can do, how? Well, with  
[37:19] control sources. So the input impedance can be modeled as a voltage control current source,  
[37:25] if you define it like this, with a gain of one over the impedance of the unit. Because according  
[37:31] to Ohm's law you have this, so it's possible to define a source like this and get something that  
[37:38] has the impedance of the measurement. In the same way you can use a voltage control voltage source  
[37:43] to implement the gain, the transfer function, when you make the gain of this control source  
[37:51] the transfer function. So these control sources will look like this. So at the output you will  
[37:58] have a voltage control voltage source that is controlled by the input the signal sent to the  
[38:04] loudspeaker or coming from the filter maybe and that will create here your measurement if you  
[38:10] put your tussle function measurement here as the value of the filter of the of the control source  
[38:17] in the same way if you have a control source current source controlled by voltage with a gain  
[38:25] of one overset, then the impedance seen from this side would be the input impedance of the unit.  
[38:34] This idea works, but there is a technical difficulty, which is that there is not enough  
[38:40] space in the value field of these sources to put all your measurements. So we have to do this,  
[38:47] not this way, but in a slightly different way. We still use this idea, but we instead include  
[38:53] the source as a text file. This text file is produced by a function that you will get  
[39:02] in this C file. So in this function you introduce your measurements, could be either input impedance  
[39:09] or transfer function, and then you get a text file that you can include in your LTSpice file.  
[39:16] And this filter, sorry, this LTSpires is the same as this one, but you cannot see the sources  
[39:26] they are included in the files.  
[39:30] You might have to edit these text files in order to change the names of the control sources.  
[39:36] If you have several units, you should have three of these circuits in your design with  
[39:43] different filters or maybe active passive filters. So this will have different label names and  
[39:48] different names of the sources. So you will have to edit labels and filter names. That's the first  
[39:55] line of these text files that you get from Mazda to LTSpice function. You also get in this package  
[40:04] this LTSpice blank file for you to use. Some tips about this. I already mentioned that you have to  
[40:18] change the labels. So another tip is this resistor is not the output impedance or anything like that.  
[40:29] It's just any resistor because the output here is a voltage source. So in order to get the voltage  
[40:35] here as the result of all these effects any resistor will do because this will impose the  
[40:40] voltage. Another thing is you will need three of these for your three units. You need to mix these  
[40:48] p-outs from the three units so you can create an extra control source that will assemble these  
[40:57] three outputs. It will sum them and then will create a sum of these units. If you  
[41:03] If you want to change polarity of one of them, you can change the sign there of this contribution.  
[41:12] Another thing is distance compensate the input impedance, only the transfer functions.  
[41:21] It doesn't make sense compensating the distance for input impedances.  
[41:29] And then what about digital filters?  
[41:32] provide also a package with another function, digitalCrossover, and this function you decide  
[41:42] the crossover frequency for the digital filter and whether you want one or two of these blocks,  
[41:47] these are called biquads, and you can assign with one or two, you would get a different  
[41:53] roll-off. So when you make this decision you run this function and from it you get two strings,  
[42:01] One string is the string you have to put in the  
[42:05] crossover control program  
[42:09] Remember there was a window when you click on the advanced  
[42:13] option. So you paste that there and you get that filter.  
[42:17] And you also get a string that you can use on these filters, sorry on these  
[42:21] control sources. And that string will make this  
[42:25] behave the same as the DSP.  
[42:29] the analog equivalent of the digital filter you are designing. So in this way you could have the  
[42:36] same in the LTSpires and in the MiniDSP box. A remark here, I have commented out the including  
[42:47] of the input impedance in this example, you also get this example, and this is because  
[42:53] this is amplified, this goes through an amplifier, it's not included here but it's assumed that there  
[42:58] is an amplifier and therefore this immune or the output impedance of the amplifier is so high that  
[43:05] it doesn't matter the input impedance of the loudspeaker so this is not relevant here. Finally  
[43:18] you have to perform a listening test in the in the listening room there is a loudspeaker listening  
[43:25] room it follows this IEC standard and is meant to be a regular room a regular living room  
[43:33] so the standard specifies size, operation time, what place the loudspeakers and so on,  
[43:40] and you can put your loudspeakers there, listen to them and run a test. This test  
[43:49] should not be very complicated, it's a questionnaire with questions about the  
[43:54] performance of the loudspeaker, how you feel the sound to be. The only thing is that it should be  
[44:02] methodical. You can inspire yourself in this book but it's something that you could invent  
[44:09] some questions but don't just listen to the box but do it methodically. Choose test subjects,  
[44:16] it could be the group members or other people you can recruit and have them go through the  
[44:22] questionnaire in a methodical way and then present the results in a kind of a statistic  
[44:28] in order to evaluate your design. You will have connections outside the listening room  
[44:38] where you can put some source, you can choose the signal you want to use,  
[44:45] you can bring your own music or use CDs or whatever. And then inside the listening room  
[44:52] you will only have a chair with the subject and the box or boxes and the passive filter.  
