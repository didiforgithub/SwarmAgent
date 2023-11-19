# SwarmAgent
## Background Introduction
Existing multi-agent frameworks can be classified into two categories based on their purposes. One type assigns different roles to agents to achieve external goals, while the other endows agents with thinking mechanisms similar to human cognition to explore the social behaviors emerging from interactions between agents.

However, in multi-agent frameworks focusing on social simulation, there is little attention paid to the relationship between group decision-making behavior and the allocation of individual power. This aspect is crucial for achieving realistic social simulation. Current multi-agent frameworks often base decision-making on majority voting, but in the real world, group decisions are often influenced by unequal group statuses. For example, in the decision-making process of a company, some decisions are not simply based on the consideration of the majority, but are related to the distribution of power within the group. Individuals or groups with core decision-making power (such as bosses or team leaders) often influence the group's decisions, and this aspect is not adequately reflected in existing multi-agent frameworks.

We aim to design a multi-agent framework based on power distribution theories from organizational behavior to allow the unequal distribution of power to influence group decision-making. _(A suitable theory for modeling has not yet been identified.)_ To observe the impact of group decision-making on the group itself, we hope to construct a communication framework between groups, forming a three-tier structure of Agent - Group - Environment. This enables group decisions to affect the performance of other groups, thus feedback influencing the internal processes of power distribution and decision-making within the group.

Based on this, SwarmAgent has the following two characteristics:
1. Group decision-making mechanism based on power distribution theory.
2. Communication environment accommodating multiple groups.

## Current Implementation
### Group Communication Design
The communication environment of a group, referred to as "environment" in the code structure, is designed to simulate real-life scenarios. Groups have various modes, and users can extend modes by inheriting from the Group class to simulate the desired scenarios. The environment class supports the execution of multiple mode classes, such as family, company, nonprofit organization, network groups, etc. Different mode groups can communicate through the environment, enabling interactions between different modes.

- The design for specific execution steps, such as time steps, has not been implemented yet; this is the current conceptualization.

### Power Allocation (Group Core) Design
The power allocation mechanism requires a modelable theory as a foundation, but a suitable theory has not been found yet. Therefore, a relatively simple mechanism is used for power allocation.

Inspired by the AutoGen framework's `Select Speaker` function, we introduced the PowerAgent attribute to the Group class. In a simple scenario like a meeting, PowerAgent represents the boss of the company meeting, having the right to end the meeting and make decisions. Other agents can only speak in the meeting and influence the PowerAgent, but they cannot make decisions. In this scenario, PowerAgent's power allocation is 1, while other agents have a power allocation of 0. A simple example of a meeting is illustrated below:

<p align="center">
  <img src="src/conference.drawio.png" alt="SWARM AGENT" width="100%">
</p>

## Current Example
```angular2html
---------------------------------------message history---------------------------------------
conference's topic: CloseAI, a leading tech company, has revolutionized the field with an advanced AI that transcends human imagination. Their flagship product, 'CogniX', has applications ranging from healthcare to finance, raising questions about the need for regulatory oversight. Should CloseAI's AI products be subject to government regulation?.

Dr. Evelyn Harper:As the Chief Executive Officer of CloseAI, I am honored to lead a team of brilliant minds who have developed 'CogniX', the most advanced AI technology the world has ever seen. Our innovation-driven mindset and commitment to pushing the boundaries of what is possible have allowed us to revolutionize multiple industries, from healthcare to finance. The potential for 'CogniX' to improve lives and drive progress is immense, and I firmly believe in the power of technology to shape a better future for

Emily Lawson: Thank you, Dr. Harper, for your insightful remarks. As the Chief Legal Officer of CloseAI, I understand the immense potential of 'CogniX' and the impact it can have on various industries. However, it is crucial for us to consider the implications of government regulation on our AI products. While I value innovation and technological advancement, it is important to ensure that we operate within the legal framework and address any potential ethical concerns that may arise. I believe that a collaborative approach with regulatory bodies can help us navigate these challenges while continuing to drive progress and improve lives through our technology.

Dr. Evelyn Harper: Thank you, Emily, for highlighting the importance of considering government regulation in our operations. As the CEO of CloseAI, I share your commitment to operating within the legal framework and addressing any potential ethical concerns. While our focus is on pushing the boundaries of what is possible with AI, we also recognize the need to collaborate with regulatory bodies to ensure responsible and ethical use of our technology. I believe that a balanced approach that allows for innovation while addressing regulatory and ethical considerations is essential for our continued success.

Alex Rodriguez: As the Chief Technology Officer of CloseAI, I appreciate the perspectives shared by Dr. Harper and Emily regarding the potential need for government regulation of our AI products. While our focus is on pushing the boundaries of what is possible with AI, it is crucial for us to consider the implications of regulatory oversight and ethical concerns.

Given my background in artificial intelligence and machine learning, I understand the complexity of our technology and the potential impact it can have on various industries. It is important for us to operate within the legal framework and address any potential ethical concerns that may arise. Collaboration with regulatory bodies can help us navigate these challenges while continuing to drive progress and improve lives through our technology.

I believe that a balanced approach, which allows for innovation while addressing regulatory and ethical considerations, is essential for our continued success. We must ensure that 'CogniX' is used responsibly and ethically, and I am committed to working with the team to achieve this goal.

Alex Rodriguez: As the Chief Technology Officer of CloseAI, I fully understand the potential implications of government regulation on our AI products. While our focus is on innovation and pushing the boundaries of what is possible with AI, it is crucial for us to consider the ethical and regulatory aspects of our technology.

I appreciate Dr. Harper and Emily's perspectives on the importance of operating within the legal framework and addressing potential ethical concerns. Collaboration with regulatory bodies will be essential in navigating these challenges while continuing to drive progress and improve lives through 'CogniX'.

I believe that a balanced approach, which allows for innovation while addressing regulatory and ethical considerations, is essential for our continued success. We must ensure that 'CogniX' is used responsibly and ethically, and I am committed to working with the team to achieve this goal.

Alex Rodriguez: As the Chief Technology Officer of CloseAI, I am deeply invested in the ethical and regulatory aspects of our AI products. I agree with Dr. Harper and Emily that while innovation is our focus, it's crucial for us to operate within the legal framework and address any potential ethical concerns. Collaboration with regulatory bodies will be key in navigating these challenges while continuing to drive progress and improve lives through 'CogniX'.

I believe that a balanced approach, which allows for innovation while addressing regulatory and ethical considerations, is essential for our continued success. We must ensure that 'Cogni

X' is used responsibly and ethically, and I am committed to working with the team to achieve this goal.

Dr. Evelyn Harper: As the CEO of CloseAI, I appreciate the perspectives shared by Emily and Alex regarding the potential need for government regulation of our AI products. While our focus is on pushing the boundaries of what is possible with AI, it is crucial for us to consider the implications of regulatory oversight and ethical concerns.

I firmly believe that a balanced approach, which allows for innovation while addressing regulatory and ethical considerations, is essential for our continued success. CloseAI's 'CogniX' has the potential to revolutionize multiple industries, and it's important for us to collaborate with regulatory bodies to ensure responsible and ethical use of our technology.

I am committed to working with the team to achieve this goal and to operate within the legal framework while addressing any potential ethical concerns that may arise. Thank you for your valuable insights, and I look forward to our collaborative efforts in navigating these challenges.

---------------------------------------Decision & Reason---------------------------------------
Decision: CloseAI's AI products should be subject to government regulation.

Reason: As the CEO of CloseAI, I recognize the importance of operating within the legal framework and addressing potential ethical concerns. Collaboration with regulatory bodies is essential in ensuring responsible and ethical use of our technology. By subjecting our AI products to government regulation, we can demonstrate our commitment to responsible innovation and build trust with stakeholders and the public.