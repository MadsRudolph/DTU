---
course: "34870"
type: transcript
lecture: 6
source: "Slides/34870_Lecture_6A_E26.mp4, 6B, 6C"
---
# Lecture 6 — transcript of the commented slides (6A, 6B, 6C)

> [!info] Machine transcript
> Whisper large-v3 (faster-whisper, GPU), English forced, metrology vocabulary prompt. VCH speaks with a strong accent, so expect word slips. Timestamps are mm:ss into each part's own video. The note: [[Lecture 6 - Microphone Scattering, Metrology & Calibration]].

## Part 6A

[00:11] In this slide we introduce the concept of free-field microphones. Free-field microphones are used both in audio and measurement and they are designed to compensate for the change in the sound field introduced by placing the microphone in the sound field.  
[00:28] When a sound field is arriving normally, especially normally to a microphone, then the pressure on the diaphragm experiences an increase, especially at high frequencies.  
[00:42] This is due to the reflection of the wave on the diaphragm and also to the scattering around edges of the diaphragm and the body of the diaphragm.  
[00:51] We'll be explaining this in much more detail later on in this course.  
[00:58] In many situations we don't have this overpressure as described before.  
[01:02] One such example could be when you flash mount a microphone on a surface.  
[01:10] In this case you might argue well there is a reflection on the plane so you have a reflected  
[01:14] wave. Yes, but this happens at all frequencies equally because we don't have an exposed body  
[01:20] of the microphone. It's a large plane that we assume is larger than the wavelength in all  
[01:27] cases we just have an increase to double pressure and therefore there's no difference between low,  
[01:33] mid or high frequencies. These microphones should not be compensated for the effect of the sound  
[01:39] field. This same effect occurs in small cavities and also in diffuse fields that have a very  
[01:48] similar characteristic that it's not really overpressure in that case. We mentioned in  
[01:56] previous lectures that the effect of the microphone in the sound field is very important because the  
[02:01] sound field is changed and our measurement can be changed as well. So let's describe conceptually  
[02:09] first what effects are at play when this happens. We have an incident wave that is hitting  
[02:17] a microphone, a diaphragm, normally through the axial direction. So the first effect we have  
[02:23] is a reflected wave. This is the same that we have when a plane wave hits an infinite plane.  
[02:30] In that case we have a doubling of pressure if the plane is totally hard. But here we don't have  
[02:35] a plane, we have a finite surface, the diaphragm. So this effect will only be true at very very high  
[02:41] frequencies where the wavelength is much smaller than the diaphragm. And the fineness of the  
[02:49] cylinder creates a diffraction, a diffracted wave that comes from the edges and can be thought of  
[02:56] secondary source or secondary sources around the edge that interfere with the other waves we have  
[03:02] here. So it's a combined effect of all these contributions. How does this play out in the end?  
[03:12] So we will have a response of this kind. This is a numerical calculation as we will see.  
[03:18] So in the first place, we have an increase in pressure at the center of the diaphragm due to the reflected wave.  
[03:25] But a doubling of pressure would only go as far as 6 dB. That's a doubling in dB.  
[03:31] The extra pressure we have here is due to the diffracted wave.  
[03:35] At some point we have a maximum. This is because we have a constructive interference.  
[03:41] But as we go up in frequency we reach a point where we have a destructive interference between edge sources and the incident wave.  
[03:51] So this effect will repeat itself as you grow in frequency and you can prove that this maxima and minima are occurring at this radius of diameter to wavelength.  
[04:05] This is because of the reflection of the edge sources.  
[04:11] This we will see also for loudspeakers in buffers.  
[04:15] So you have to remember this because there will be a revisiting of this effect when we talk about loudspeakers.  
[04:25] So, in short, the total scatter wave is the combination of a reflected wave and a diffracted wave.  
[04:32] For microphones, we are not truly interested in all these come effects, because microphones normally don't work much more beyond this first maximum.  
[04:42] So it would be sufficient, as we will see later, to consider the reflected wave for microphones.  
[04:51] In order to prove the points in the previous slide, I have introduced here a numerical calculation.  
[04:57] Numerical calculation is much closer to the real-life effect than these abstractions I have mentioned.  
[05:05] So, we have again a microphone and a plane wave that hits normally to the diaphragm.  
[05:13] So, this is the response calculated numerically. So, how does the sound field look like at different points?  
[05:21] So at low frequencies, the effect of the microphone is not seen by the sound field almost.  
[05:33] So you see here that we have a progressive sound wave and it's almost undisturbed by the microphone.  
[05:39] This is a low frequency then.  
[05:41] As the frequency grows, we are beginning to observe an increase in pressure on the diaphragm.  
[05:51] And this is due to the reflection on the diaphragm by now, but as you continue increasing the frequency, you reach a point where you have a maximum of pressure.  
[06:03] And this is the result of the combined effect of reflected wave and the constructive interference of the diffracted wave from the edges.  
[06:13] So you can almost see here the effect.  
[06:17] If you continue, then you reach a minimum. In this case, you will see that directly,  
[06:22] exactly directly on the diaphragm, you have a very low pressure. And that's because these  
[06:27] edge sources cancel out with the incident wave at this point. And you can go on this way  
[06:35] and find another maximum, where you will have more maxima and minima over the diaphragm.  
[06:40] And finally what we can say here is that all this looks very interesting but if you try to measure  
[06:51] with a microphone then you will have a hard time to get these responses at very high frequencies.  
[06:58] This is just the pressure calculated on a hard cylinder. So the microphone doesn't really work  
[07:04] beyond more or less this point because non-uniform pressure on the diaphragm would give a  
[07:10] a wrong output or almost zero output. So we don't use microphones above this point where we have the  
[07:19] first increase. For this reason from now on all the development we will have only considers  
[07:24] reflection not the diffraction of the edges. How do we model this? Because our analogy circuits  
[07:32] cannot account for that so easily. They are made for mechanical lamp elements,  
[07:37] algorithmic elements, electrical circuits and so on. So, we use a Leach method or an adaptation  
[07:44] of it. I recommend rather to use the description here in the slides, but nevertheless I have uploaded  
[07:52] Leach description. But keep in mind that this is an approximation, it's not real, it's a way  
[07:59] to get this to be a circuit. In this description we simplify the phenomenon  
[08:07] saying that we have an incident wave with a volume velocity and a reflected wave with another volume  
[08:13] velocity, uR, and then at this boundary here we have a radiation impedance and an input impedance  
[08:21] of the transducer. Okay, here we will use some expressions, in principle meant for plane waves  
[08:33] arriving and reflecting normally on a plane. These expressions you can find in basic acoustic books  
[08:40] like fundamentals of acoustics that we used in previous courses. Here you have the expression  
[08:45] of an incident wave, a plane incident wave, the volume velocity and reflected volume velocity  
[08:53] as a function of the impedance of the diaphragm or the plane. The reflected pressure would be  
[09:01] the product of the radiation impedance times the reflected volume velocity. So if we want to get  
[09:07] the pressure on the diaphragm, then we have to sum the incident pressure and the reflected pressure  
[09:13] using the expressions that we have before. And doing so, we get this expression,  
[09:23] but we can do further approximations. Usually the impedance of the diaphragm  
[09:28] is high, so one can be assumed that it's a hard surface, and then that would mean that ZAD, the  
[09:35] impedance of the diaphragm input impedance of the microphone would be approximated as infinite  
[09:41] therefore the reflection factor coefficient is one and the volume velocity of the reflected  
[09:47] wave is equal to the volume velocity of the incident wave and then this expression here  
[09:51] can be simplified like this this expression relates the pressure on the diaphragm with the  
[09:58] incident pressure in the sound field so this is what we have to  
[10:02] simulate or include in the circuit somehow. As to the radiation impedance, we notice that  
[10:10] this effect happens almost always in the high frequency due to the size of the microphones.  
[10:16] This usually happens at the high end of the frequency response of the microphone. This  
[10:22] means that the radiation impedance that, if you remember, was modeled by a network with four  
[10:27] components to resistors, a coil and a capacitor, can be approximated as one of the components,  
[10:32] one of the resistors. The coil would be an open circuit and the capacitor would be a short circuit,  
[10:39] leaving only the Ra2 component. So we can put that Ra2 here and that would be a function  
[10:46] that is called in Leitch Ts. This function multiplied by Pi gives us the actual pressure  
[10:52] on the diaphragm. This is the circuit proposed by Leach in order to model this normal plane wave  
[11:01] incident on the microphone effect. The new element here is this control source. The value of the  
[11:08] control source is the incident pressure, which in this circuit is called P01, divided by the value  
[11:15] of this component. This is the radiation impedance, as I said before. It can be demonstrated that  
[11:21] including this generator here is equivalent, it's the same as not including it and having a value  
[11:27] here of incident pressure times the ds as defined in the previous slide. What does this generator  
[11:35] do? It implements the pressure increase at high frequencies as we described only to this point,  
[11:42] then it decreases but not in the same way as it actually does in the sound field. So it's not a  
[11:49] true representation beyond the maximum here, but it's useful for circuit analysis.  
[12:00] This is the LTSpice version of the same circuit, as you can see, and this would be the  
[12:07] acoustical part of the transducer circuit that contains the radiation impedance and the  
[12:13] incident pressure. This is without the effect of the sound field. We have the response of the  
[12:20] the microphone. What happens if we include the generator? It's the generator  
[12:24] that mimics the sound field. This is what happens. We have an increased  
[12:31] sensitivity at high frequencies. You can see here in LTSpice we need to feed, in  
[12:38] this voltage control generator, we need to feed the incident pressure which we  
[12:42] connect through this label here. Labels are equivalent to wires so this is the  
[12:46] as having a wire all the way to this place. At this point you may solve problem 2 which is an  
[12:56] LTSpice circuit representing the condenser microphone. Finally we arrive to the LTSpice model.  
[13:04] You can use this in order to do your exercises and also your lab exercises. As you can see here  
[13:13] this is the same circuit we have from Leech. We have used labels to connect the generators. This  
[13:20] This is the condenser transducer, this is the mechanical acoustic transducer affected  
[13:27] by the surface, and here we have developed a radiation impedance into all these components.  
[13:32] This is interesting in this microphone because we work at high frequencies and therefore  
[13:37] we need the components.  
[13:39] We have added here the generator that mimics or represents the effect of the sound field.  
[13:46] You only include this generator if you want to include this effect, not if the microphone  
[13:52] is used in other conditions, for example an actuator.  
[13:54] Remember this for your exercises.  
[13:59] This would be a typical response calculated with LTSpice.  

## Part 6B

[00:04] Welcome to the sixth lecture in the course on electroacoustic transducers and systems.  
[00:09] This lecture is about metrology and acoustic calibration.  
[00:12] What is metrology? Metrology is the science of measurement.  
[00:19] Here is the definition, official definition, from the BIPM.  
[00:23] The BIPM is the Bureau International of White Sand Measures.  
[00:27] It is an organization which is originated by a world agreement between all countries  
[00:35] countries doing measurements in terms of units and references for measurement the importance  
[00:41] of measurements is stressed in this statement from lord kelvin in the 19th century  
[00:48] you only can understand things when you measure them measurements important measurements are  
[00:57] not only important for scientists researchers politicians measurements are part of everyday  
[01:06] life for everybody. When you buy things, when you use your car, there are many examples of the  
[01:13] importance of good measurements. Measurements have a big role on industry, on commerce,  
[01:22] and they have to be consistent all over the world, otherwise things like exchanging goods or  
[01:29] or selling products cannot be done properly.  
[01:33] But as you can think of some examples in acoustics, think for example  
[01:37] on consultancy about noise measurement.  
[01:41] Noise regulations state limits for noise  
[01:45] and these limits have to be measured properly, otherwise there are legal implications  
[01:49] on it. This is just an example of possible  
[01:53] implications of good measurements.  
[01:55] Some history of metrology. How the current system was originated. Well, in the old days, the systems of measurement were based on local units like body parts like the foot of the king.  
[02:10] There were different units for different things that you could measure. So it was quite chaotic.  
[02:16] During the French Revolution, it was proposed that the measurements should be based on same  
[02:23] units and based on a decimal system, where the units were multiples of 10.  
[02:28] During the 19th century, this system was extended over many countries.  
[02:36] In 1875, the Treaty of the Metre Convention was signed and the Rural International of  
[02:42] Weights and Measures was created.  
[02:45] In 1960, the International System of Units that we use today was established, and recently, in 2019, there was a total redefinition of the system of units.  
[03:01] They are not anymore based on objects, but they are based on the natural constants of physics.  
[03:08] Just to get an idea of how extended the National System of Units is today, there is a map showing  
[03:18] in red the countries that use another system, that's the United States of America, Liberia  
[03:25] and Burma.  
[03:27] And Burma is about to change to SI.  
[03:31] So, the SI is dominant all over the world.  
[03:36] Here is a joke from the internet showing a kind of difference between the imperial system in USA and the international system of units, which is much more logical in many respects.  
[03:47] So, what is this new definition of the international system of units?  
[03:53] This definition is based on seven natural constants.  
[03:57] For example, the speed of light in vacuum, Planck constant, etc.  
[04:01] These constants are given a fixed number as a value by definition, and then all the rest of quantities that you could measure are based on those values.  
[04:13] So all the uncertainty of the system depends on how well one can measure the physical constants.  
[04:20] For example, the speed of light is related to speed meters per second.  
[04:25] The definitions of length and time are related to it.  
[04:29] It's just an example. Before this new definition, the whole system was based on these base units,  
[04:38] seven base units, that are kept still as a definition. They are all based on, again,  
[04:50] on the physical constant. There are some rules, practical rules, to unify criteria in expressing  
[05:00] units. So, as you can see here, you can read in detail in the ISAI brochure that you can download  
[05:09] from the BIPM website and you have also in Learn. There are rules like how you write the units.  
[05:20] For example, the abbreviation of a unit will have a capital if it corresponds to a person.  
[05:25] It will not have a capital if it's extended or if it's the full name.  
[05:28] There are prefixes to express larger or smaller values, normalized as well, those in this table.  
[05:37] And here you have some examples of use of units. You have to try to stick to these rules so everything is consistent.  
[05:48] Let's talk now about uncertainty in measurement. We start with a few basic concepts.  
[05:57] All these concepts are taken from the vocabulary of metrology in the B.I.P.M.  
[06:06] Everything is normalized in metrology.  
[06:08] The definition of measurement uncertainty is a parameter which is associated with a measurement.  
[06:15] And this parameter characterizes the measurement in terms of dispersion.  
[06:19] It tells us how certain, how sure can we be that this parameter is close to the true result.  
[06:26] Which, by the way, the true value is defined as the measurement result that we seek.  
[06:32] And we will never know it because it is impossible to get it totally precise.  
[06:37] So we define measurement error as the difference between this true value and the result we get.  
[06:43] And then two interesting concepts, repeatability and reproducibility.  
[06:47] are not the same. Repetability is the spread of results when we measure again and again under  
[06:53] the same conditions, this is important. And reproducibility is the spread of results when  
[06:58] we measure under different conditions. Different conditions can be that we change some equipment,  
[07:03] we change the operator, we change something in the measurement. It should not matter,  
[07:07] but in the end it matters. Some basic concept of metrology is traceability.  
[07:15] Traceability gives you the uncertainty of any measurement referred to the highest standards  
[07:20] through a chain which is the traceability chain. So for every magnitude there is a  
[07:29] national standard that is the absolute reference for this magnitude. For example for the kilogram  
[07:38] or the meter, also for the acoustic Pascal. So this national standard, through calibration,  
[07:45] sets the secondary standards. And the secondary standards set working standards. So this all  
[07:51] goes down to the everyday measurement. It could be the fruit in the supermarket, whatever. So  
[07:59] everything is linked in the end to these national standards. And naturally, the national standards  
[08:05] have the less uncertainty of all. They work a lot to get this uncertainty as low as possible  
[08:10] because this has an influence on all measurements in the chain. If you work in a company, many big  
[08:19] companies that do measurements and produce products that need to be measured have their own  
[08:25] traceability chain. They refer to the country chain but they might have their metrology labs  
[08:33] and they may have their standards that they need to calibrate so you will meet this system if you  
[08:39] work for a big company doing measurements how do all the countries compare and organize themselves  
[08:47] to keep the standards we talk about national standards the national institutes every country  
[08:52] has a national metrology institute coordinate together in the vipm there are regional  
[08:58] organizations like for example Euromed in Europe where DFM that's the Danish  
[09:04] metrology institute or PTV in Germany same in Spain or MPL in UK that coordinate in this  
[09:10] organization to maintain their standards properly. There are other regional organizations they  
[09:17] coordinate regionally and there's also coordination globally. How is this coordination made? One of the  
[09:23] The main tools for this are key comparisons, so these national standards need to be compared  
[09:29] with each other.  
[09:30] There is not a world standard, so these national standards make peer comparisons so they see  
[09:37] how close are from each other and then decide how this unit is maintained and kept together.  
[09:45] So there are regional comparisons, there are worldwide comparisons, there are also comparisons  
[09:50] in acoustics where sets of microphones travel and measure in different countries and this  
[09:57] keeps out of the activity of the BIPM and similar organizations. Now we talk about acoustic  
[10:06] metrology. Maybe you wonder how the acoustic pascal is defined. It has to refer in the end  
[10:13] to the basic units and these constants I talk about. But in particular for acoustics the  
[10:21] The standard is not an object, it's a method in which we use microphones, we use three  
[10:30] microphones in principle for this measurement, and these are condenser microphones.  
[10:34] Condenser microphones are reciprocal, this means that it's possible to use the microphone  
[10:38] as a microphone, but it's also possible to use the microphone as a kind of loudspeaker,  
[10:44] using it in the other direction.  
[10:47] In principle you can do this with any acoustic transducer, also with loudspeakers working  
[10:50] as microphones. But if you do this with this microphone thing you can place one microphone  
[10:56] as a loudspeaker radiating sound and the other as a receiver as a microphone. Microphones have  
[11:03] the same sensitivity when they radiate and when they receive. So if you do this then you can  
[11:07] measure the input current and the output voltage and you can measure your three microphones in  
[11:14] pairs so you end up with three measurements. With these three measurements you get three equations  
[11:20] and then you can deduce the sensitivities of the three microphones.  
[11:24] So the standard is the method, not the microphones themselves.  
[11:29] You can use any microphones and include an extra microphone that will be sent to secondary calibration.  
[11:36] There are two versions of this measurement.  
[11:38] You can put these two microphones in a cavity and that's called pressure and reciprocity calibration.  
[11:44] And you can place them in an echo chamber and that's called free-field reciprocity calibration.  
[11:49] This is a sketch of how you place the microphones in the pressure-reciprocity calibration in a cavity.  
[11:58] It is normal to use several couplers with different lengths to cover the whole frequency range.  
[12:05] However, this system has difficulties at high frequencies because the sound field inside the cavity becomes more complicated  
[12:13] and the results are not so reliable, have much more uncertainty at high frequencies.  
[12:18] This is a system, an off-the-shelf Brunegger system that is used in Mexico.  
[12:27] As you can see, the system has microphones. These are special microphones made for this primary calibration.  
[12:33] It's only Brunegger doing them. And these are the couplers of different lengths.  
[12:38] The couplers are placed here. One microphone is screwed here, the coupler is put on top,  
[12:43] and then the other microphone is put on the other direction on top of this.  
[12:47] then everything is sealed in a chamber that is regulated to have sea level pressure.  
[12:56] This is cumbersome, for example in this Xenam setup the pressure at this lab is only 80% of  
[13:03] sea level, so it has to pump the air and make it much higher pressure here than in the laboratory.  
[13:11] The temperature is measured at the same time, so it's much more demanding measuring at this level  
[13:17] This is the system we have in Denmark, which is in our building below the classroom.  
[13:26] This is a homemade, because there has been research being done on this, so this is a  
[13:30] more advanced system.  
[13:31] It is possible to visit it, you can contact Salvador Barrera and organize a visit if you  
[13:37] are interested.  
[13:38] This is the sketch of the system, where you have the microphones, the preamplifiers, the  
[13:45] of the ambient conditions and the equipment around it.  
[13:51] This is the sketch from the free-fill reciprocity calibration.  
[13:53] There has to be an antiquated chamber, there is an antiquated chamber downstairs, specialized  
[13:59] on this kind of measurement, and then the microphones are placed there in the open.  
[14:05] This is the chamber, it's a smaller chamber than we are used to because the setup is smaller.  
[14:11] This is the sketch from our measurement.  
[14:17] some concepts about uncertainty measurement. You will need this for your exercise today.  
[14:23] It's a simple exercise but it shows how meteorologists estimate the uncertainty  
[14:27] of a measurement. So a measurement is described by its equation, the model of the measurement.  
[14:35] It's a mathematical expression that relates input quantities with the output. For example,  
[14:41] we say if we want to measure area then we have to measure the width and the height  
[14:44] and then we get the area. That's this expression. When we do this measurement, then we have to  
[14:51] obtain an estimate of the mean of the result. This would be an estimate that would be a function,  
[14:58] through this function, of the input variables. So these are random variables, these are the means,  
[15:05] we obtain the mean of the result like this. So in this case we have the mean of your measurements  
[15:11] the width, the mean of your measurements of the height and then you would get the value of the  
[15:15] area that would be the mean hopefully of the distribution of this area random variable.  
[15:22] How do you get the deviations of the measurement from the deviations of the input variables?  
[15:29] There is this expression, this is all explained in the GUM as stated before. This is the most  
[15:35] common method for obtaining the what is called combined standard uncertainty which is this term  
[15:41] here. We assume no correlation between the input variables, you just have to obtain what we call  
[15:48] sensitivity coefficients, which is how much the result varies with respect of the variation of  
[15:54] one of the input variables. This you can obtain by taking the derivative with respect of that  
[15:59] variable of the function defined in the measurement. You could also vary one of the inputs and see what  
[16:04] the effect is on the output. That would be a finite difference approximation. And then you have to have  
[16:10] the uncertainties of the inputs. Through the central limit theorem we can say that the  
[16:20] distribution of the output tends to be a normal distribution. So this is what you will be using  
[16:26] in your exercise. If you have a correlation between these variables then you would have to  
[16:32] need to use a more complicated expression like this. So you use a covariance matrix instead  
[16:40] with correlations between variables. Still this is possible, but it's not in your exercise today.  
[16:47] So in your problems 1 and 2 today, you have a very simple uncertainty estimation,  
[16:56] and also you can test it because it's a condenser microphone on LTSpice,  
[17:01] the LTSpice from previous lecture for condenser microphone, and test that variations follow the  
[17:07] same you calculated in problem 1. Usually condenser microphones don't show a  
[17:15] distinct peak in the frequency responses, in their sensitivities. If we have a  
[17:20] measurement and we want to deduce resonant frequency and Q factor, let's have this  
[17:25] example where we have the magnitude and phase of a measurement with corresponding  
[17:31] scales here, how do we get the resonant frequency and quality factor? Well, first  
[17:38] First of all, we look at the phase and we detect the phase at which there is a drop  
[17:45] of 90 degrees from mid frequencies.  
[17:48] This is the frequency where we have the resonance.  
[17:50] In this way, we detect the resonance.  
[17:52] Here is a level of 10 kHz in this example.  
[17:57] Then we have to realize that if you replace the resonance frequency in the transfer function,  
[18:02] then this, as compared with the sensitivity at mid-frequencies, is the quality factor.  
[18:10] So, if this scale is linear, then we just have these values at resonance and at mid-frequencies,  
[18:16] and we can obtain the Q-factor directly.  
[18:18] If the scale is in dBs, then we can still deduce from the dB difference the Q-factor, the quality factor.  
[18:27] But notice that the Q can be less or more than 1.  
[18:31] Therefore this drop could be a drop or could be an increase, so it could be less negative or positive, therefore less than one or more than one.  
[18:44] Finally we arrive to the LTSpice model of the microphone.  
[18:48] You can use this in order to do your exercises and also your lab exercises.  
[18:55] As you can see here, this is the same circuit we have from Leech.  
[18:59] We have used labels to connect the generators.  
[19:02] This is the condenser transducer.  
[19:06] This is the mechanical acoustic transducer affected by the surface.  
[19:11] And here we have developed a radiation impedance into all these components.  
[19:14] This is interesting in this microphone because we work at high frequencies and therefore we need the components.  
[19:21] We have added here the generator that mimics or represents the effect of the sound field.  
[19:28] You only include this generator if you want to include this effect, not if the microphone is used in other conditions, for example an actuator.  
[19:36] Remember this for your exercises. This would be a typical response calculated with LTSpice.  
[19:49] So in your problems 1 and 2 today, you have a very simple uncertainty estimation.  
[19:56] And also you can test it because it's a condenser microphone on LTSpice.  
[20:00] LTSpice, the LTSpice from previous lecture for condenser microphone and test that variations  
[20:05] follow the same you calculated in problem 1. In this last part of the lecture, we're going to  
[20:13] talk about calibration devices. These are devices that are used to verify that the microphone is  
[20:19] working properly and maybe adjust to adapt for the ambient conditions. This is not properly  
[20:27] a calibration, a metrological calibration, but it's a verification. Some of these devices  
[20:32] are called calibrators. There are two devices that correspond to this. The calibrator, which  
[20:38] is a field instrument used in field measurements. It's specified in many standards of measurement  
[20:45] that you have to use the calibrator for proper measurements. And then the pistophone. The  
[20:50] pistophone is a laboratory device. It's not for field use. It's also used as part of calibrations.  
[20:57] What we try is that the impedance of the of the microphone doesn't affect this verification  
[21:10] because those devices create a sound field that is known and fixed so we should try that the  
[21:17] microphone doesn't alter these fixed values. The first of these two devices is called  
[21:24] microphone calibrator which should be called a verificator because it's used to verify in the  
[21:30] fill the measurements made by a microphone. So basically it is a cavity  
[21:35] with a hole where you can place the microphone to be verified and then it  
[21:41] can have a source, a loudspeaker and a control microphone. It works in this way  
[21:48] the loudspeaker creates a signal, a single frequency and with a given level  
[21:53] and this signal is controlled by a feedback microphone so the level is  
[21:57] correct. The values for these devices are usually 250 Hz and 1 kHz and then  
[22:06] the values can be 1 or 10 Pascal. There are multi-frequency calibrators but  
[22:10] they are not very common. Usually one calibrator has a single frequency which is  
[22:15] sufficient if it's in the mid-range. The Pistophone is a more special device.  
[22:21] Pistophone doesn't have a loudspeaker, it has a piston or mechanical device  
[22:29] that moves a piston. In the same way, the cavity where this piston is has another  
[22:36] hole to receive the microphone and it has no feedback in it. Therefore, the  
[22:44] reading has to be corrected for the static pressure at this moment. One has  
[22:49] to measure the static pressure with a barometer at the same time. But these  
[22:54] devices are very stable, they always work the same and they are very good, they have  
[22:59] low uncertainty for laboratory use. They are used mainly in secondary calibration.  
[23:06] That's the calibrations you do after the main standard of calibration. We will see that  
[23:11] in the next lecture. Here are some examples of calibrators.  
[23:17] This is an old type from Blue Anchor. This is peculiar because it doesn't have a feedback.  
[23:22] The changes in the impedance of the microphone are compensated using an acoustic network  
[23:29] with a helm oscillator and two cavities in the front and in the back of the  
[23:34] moving diaphragm which is moved by a piezoelectric  
[23:38] device. This is part of your exercises today so  
[23:43] you will have to to draw the network for this.  
[23:46] More modern calibrators like this one use feedback as explained before.  
[23:53] You will use these calibrators in the LABSI exercise  
[23:57] together with the actuator. And then a pistophone example that will work something like this.  
[24:06] It's like this, so you can see it's not something that looks for field use. And this is a sketch of  
[24:13] how the piston works. It's a kind of rotating device that moves the pistons on the two sides  
[24:20] of the of this cylinder. It has a barometer in order to compensate for the change in static  
[24:30] pressure and it's more precise than the calibrator and finally it's time for the third problem here  
[24:40] and this is all for today  

## Part 6C

[00:07] We mentioned in previous lectures that the effect of the microphone in the sound field is very important, because the sound field is changed and our measurement can be changed as well.  
[00:19] So let's describe conceptually first what effects are at play when this happens.  
[00:26] We have an incident wave that is hitting a microphone, a diaphragm, normally through the axial direction.  
[00:34] So the first effect we have is a reflected wave. This is the same that we have when a plane wave hits an infinite plane.  
[00:42] In that case we have a doubling of pressure if the plane is totally hard.  
[00:46] But here we don't have a plane, we have a finite surface, it's the diaphragm.  
[00:51] So this effect will only be true at very very high frequencies where the wavelength is much smaller than the diaphragm.  
[00:59] And the fineness of the cylinder creates a diffraction, a diffracted wave that comes from the edges and can be thought of as a secondary source or secondary sources around the edge that interfere with the other waves we have here.  
[01:15] So it's a combined effect of all these contributions. How does this play out in the end?  
[01:24] So we will have a response of this kind. This is a numerical calculation, as we will see.  
[01:30] So in the first place, we have an increase in pressure at the center of the diaphragm due to the reflected wave.  
[01:38] But a doubling of pressure would only go as far as 6 dB. That's a doubling in dB.  
[01:43] The extra pressure we have here is due to the diffracted wave, and at some point we have a maximum.  
[01:50] This is because we have a constructive interference but as we go up in frequency  
[01:56] we reach a point where we have a destructive interference between edge sources and the  
[02:02] incident wave. So this effect will repeat itself as you grow in frequency and you can prove that  
[02:10] this maxima and minima are occurring at this radius of diameter to wavelength. This is because  
[02:18] of the reflection of the edge sources.  
[02:23] This we will see also for loudspeakers in buffers.  
[02:27] So you have to remember this because there will be a  
[02:31] revisiting of this effect when we talk about loudspeakers.  
[02:37] So in short, the total scatter wave is the combination of the reflected wave  
[02:42] and the diffracted wave.  
[02:44] For microphones, we are not truly interested in all these comb effects  
[02:47] because microphones normally don't work much more beyond this first maximum.  
[02:54] So it would be sufficient, as we will see later, to consider the reflected wave for microphones.  
[03:04] In order to prove the points in the previous slide, I have introduced here a numerical calculation.  
[03:10] Numerical calculation is much closer to the real-life effect than these abstractions I have mentioned.  
[03:18] So, we have again a microphone and a plane wave that hits normally to the diaphragm.  
[03:26] So, this is the response calculated numerically.  
[03:30] So, how does the sound field look like at different points?  
[03:34] So, at low frequencies, the effect of the microphone is not seen by the sound field almost.  
[03:46] So you see here that we have a progressive sound wave and it's almost undisturbed by the microphone.  
[03:53] It is a low frequency then. As the frequency grows, we are beginning to observe an increase in pressure on the diaphragm.  
[04:03] And this is due to the reflection on the diaphragm by now.  
[04:08] But as you continue increasing the frequency, you reach a point where you have a maximum of pressure.  
[04:15] And this is the result of the combined effect of reflected wave and the interference,  
[04:22] constructive interference of the diffracted wave from the edges.  
[04:26] So you can almost see here the effect.  
[04:29] If you continue, then you reach a minimum.  
[04:31] In this case, we see that directly, exactly directly on the diaphragm,  
[04:36] you have a very low pressure.  
[04:38] And that's because these edge sources cancel out with the incident wave at this point.  
[04:44] and you can go on this way and find another maximum where you will  
[04:50] have more maximum minima over the diaphragm  
[04:56] and finally what we can say here is that all this looks very interesting but  
[05:03] if you try to measure with a microphone then you will have a hard time to get  
[05:07] these responses at very high frequencies this is just  
[05:10] the pressure calculated on a hard cylinder so the microphone  
[05:16] doesn't really work beyond more or less this point because non-uniform pressure on the diaphragm will  
[05:22] give a wrong output or almost zero output so we don't use microphones above this point where we  
[05:30] have the first increase for this reason from now on all the development we will have only considers  
[05:36] a reflection not the diffraction of the edges in the literature you will see in the data sheets and  
[05:44] and applications of my microphone, you will see something called free-field correction.  
[05:51] The free-field correction accounts for the effect of the scattering of the sound field  
[05:55] by the microphone body. It doesn't have to do with the internal workings of the microphone.  
[06:01] It's an effect of the scattering.  
[06:04] When one adds this to the actuator response, one has a free-field response.  
[06:11] More or less, it's not as precise as measuring with the correct microphone.  
[06:16] This refill correction of course depends on the size of the microphone.  
[06:20] And here you have some examples in the sketches.  
[06:24] I also have here some examples from old microphones.  
[06:30] This is a one inch microphone.  
[06:32] And as you will see, the correction is drawn here for several angles.  
[06:37] It is of course higher for zero degrees incidence, that means normal incidence to the diaphragm.  
[06:43] If the incidence is not normal, then the correction is less.  
[06:48] As you can see here, for this large microphone, it has the largest microphone, normal use.  
[06:53] It's not so much use anymore.  
[06:56] The effects are very strong at 10 kHz.  
[07:00] They have a peak just after 10 kHz.  
[07:03] So if you look at smaller microphones, like half-inch microphones,  
[07:07] you can see that the effect is displaced to higher frequencies.  
[07:10] That's because the diameter of the microphone is smaller.  
[07:14] Therefore, it compares with the wavelength in another way.  
[07:18] Here you can see that the peak of the zero degree of incidence is higher up.  
[07:23] It's 20 something kilohertz, as you can see.  
[07:27] If we look at even a smaller microphone, a quarter inch, this peak is as high as 50 kilohertz.  
[07:36] These microphones can actually measure very well ultrasound up to more than 100 kHz.  
[07:43] That's yet another microphone, a quarter-inch microphone, which is extremely small.  
[07:48] It's not so much use, but it has very low sensitivity.  
[07:51] But this one can measure very high frequencies.  
[07:54] At its peak of scattering, it's around 100 kHz.  
[08:00] In a LabD exercise you will be comparing this with a measurement you will do on a mockup microphone, a cylinder made of wood.  
[08:08] In this slide you have a sketch that summarizes the effect of the size of the microphone on its properties.  
[08:19] If you have a large microphone, then you get a high sensitivity because the diaphragm is large.  
[08:26] But then you also get more disturbance of the sound field.  
[08:29] field. That means that the peak of disturbance is at a lower frequency. That means that the bandwidth  
[08:37] is narrower, the higher frequency is lower. Whereas if you have a smaller microphone with  
[08:46] less diameter, then it has less sensitivity, but then the disturbance to the sound field  
[08:53] happens at a higher frequency. And also you can measure higher frequencies with it.  
[09:03] Method for calibrating microphones, for obtaining their sensitivity response, frequency response,  
[09:09] is the actuator. The actuator consists of a metallic object that is placed very close  
[09:16] to the diaphragm, on top of it, and it's excited by an electrical DC and plus AC  
[09:26] voltage. This AC voltage carries a signal. Therefore the excitation is purely electrical.  
[09:32] There are electrical forces acting on the metallic diaphragm that move it.  
[09:36] It is not an acoustical excitation. This pressure is assumed to be uniform over the diaphragm.  
[09:41] This is not, therefore, a situation like in the free field that we just mentioned.  
[09:46] This would be more similar to mounting the microphone in a cavity, aiming for pressure.  
[09:56] This method, due to the way this hardware is constructed, is not good for obtaining the figure  
[10:00] of the sensitivity at mid frequencies. It's good for obtaining the response curl, the  
[10:07] frequency dependence of the sensitivity. We have to find this and adjust this sensitivity  
[10:14] numerically with other methods as we will see. How do we do this in practice? We have first to remove  
[10:21] the grid of the microphone and then place the actuator, this is an actuator, on top of the  
[10:27] open microphone and this is a delicate operation because the microphone when  
[10:33] it's exposed cannot be touched, it's very delicate, a single touch with the  
[10:37] diaphragm will destroy it, will destroy the microphone and these microphones are  
[10:40] really expensive so be careful with this when you do this in in Lab C. This is the  
[10:49] photograph of the setup for Lab C with the microphone and the actuator which is  
[10:55] connected to this source that mixes the DC and the AC signals. Here are some examples of microphones.  
[11:04] Microphones are designed to be used in specific conditions. For example, this Blanquer 4191 is  
[11:14] what is called a free-fill microphone. It's designed to be used in free-fill conditions,  
[11:18] which are the conditions we have when a plane wave hits the diaphragm, as we saw in the animations  
[11:24] before. So when you measure this microphone in an actuator then you get a  
[11:30] damped response because the microphone is designed to be exposed to a field that  
[11:36] increases the pressure at high frequencies. Therefore when it is exposed to what we  
[11:40] call a free field, a brainwave heating the diaphragm, then we get a more or less  
[11:43] flat response. They are designed for this purpose. This is what we call a free field  
[11:48] microphone. Its internal work is compensated for the sound field. On the other hand we  
[11:54] We also have pressure-filled microphones.  
[11:57] Pressure-filled microphones perform well in situations like the actuator, where we have  
[12:02] a uniform pressure, or cavities, or similar situations.  
[12:06] But if a microphone like this is exposed to a bling wave hitting the diaphragm, then it  
[12:12] will have an excess pressure, as we have explained before.  
[12:17] This is the pressure-filled microphone.  
[12:18] It is not compensated for free-fill conditions.  
