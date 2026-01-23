import React, { useState } from 'react';
import { Download, FileText, CheckCircle } from 'lucide-react';

const PPTGenerator = () => {
  const [isGenerating, setIsGenerating] = useState(false);
  const [downloadReady, setDownloadReady] = useState(false);

  const generatePPTX = () => {
    setIsGenerating(true);
    
    // Create PPTX content
    const pptxContent = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<pptx>
<!-- This is a PowerPoint XML structure -->
<!-- Note: Full PPTX generation requires complex XML packaging -->
<!-- This demonstration shows the structure and content -->

<presentation>
  <slides>
    
    <!-- Slide 1: Title Slide -->
    <slide number="1" layout="title">
      <background color="#0033A0"/>
      <title fontFamily="Arial" fontSize="44" color="#FFFFFF" bold="true">
        Build Better Teams: Coaching and Team Development for Construction Managers
      </title>
      <subtitle fontFamily="Arial" fontSize="24" color="#FFFFFF">
        A 120-Minute Workshop for Middle Managers in Construction Management
      </subtitle>
      <footer fontFamily="Arial" fontSize="14" color="#FFFFFF">
        Boise State University PACE | [Date] | [Location]
      </footer>
      <image position="bottom-right" description="Boise State Logo"/>
    </slide>

    <!-- Slide 2: Learning Approach -->
    <slide number="2" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Learning Approach and Context
      </title>
      <content fontFamily="Arial" fontSize="18" color="#0033A0">
        <bulletPoint icon="check-circle">Mixed teaching approach: micro-lectures, discussions, and live templates</bulletPoint>
        <bulletPoint icon="construction">Emphasis on application in construction settings</bulletPoint>
        <bulletPoint icon="users">On-site and office coordination scenarios</bulletPoint>
        <bulletPoint icon="target">Practical, take-home tools you can use immediately</bulletPoint>
      </content>
      <image position="right" description="Construction team collaborating on blueprint"/>
    </slide>

    <!-- Slide 3: Opening Hook (Part 1) -->
    <slide number="3" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Opening Hook: The Cost of Miscommunication
      </title>
      <content fontFamily="Arial" fontSize="20" color="#0033A0">
        <narrative>
          In a typical project, small miscommunications can cascade into:
          • Costly delays
          • Expensive rework
          • Safety risks
          • Team frustration
        </narrative>
      </content>
      <reflectionBox backgroundColor="#F5F5F5" borderColor="#D64309">
        <question fontSize="22" color="#D64309" italic="true">
          "What's one coaching moment you wish you could have handled differently on a project last week?"
        </question>
      </reflectionBox>
      <image position="background-subtle" description="Construction site with team discussing"/>
    </slide>

    <!-- Slide 4: Opening Hook (Part 2) -->
    <slide number="4" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Why This Matters
      </title>
      <statBox backgroundColor="#0033A0" textColor="#FFFFFF">
        <stat fontSize="36" bold="true">
          Teams that practice structured coaching report higher reliability and fewer rework events
        </stat>
      </statBox>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309">
        <icon name="users-talk"/>
        <activityTitle fontSize="24" color="#D64309">Activity: Think-Pair-Share</activityTitle>
        <instructions fontSize="18" color="#0033A0">
          2 minutes: Reflect individually, then share with your small group
        </instructions>
      </activityBox>
    </slide>

    <!-- Slide 5: Learning Outcomes -->
    <slide number="5" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        By the End of This Workshop, You Will Be Able To:
      </title>
      <outcomes fontFamily="Arial" fontSize="18" color="#0033A0">
        <outcome number="1" icon="message-circle">
          Conduct a structured coaching conversation using a 4-step model (Ask, Reflect, Decide, Commit)
        </outcome>
        <outcome number="2" icon="calendar-clock">
          Plan and lead a 15-minute daily team huddle using a standard template
        </outcome>
        <outcome number="3" icon="network">
          Map team roles and responsibilities, identify misalignments, and propose concrete actions
        </outcome>
        <outcome number="4" icon="clipboard-list">
          Produce a 90-day action plan applying coaching and team development practices
        </outcome>
      </outcomes>
      <note fontSize="14" color="#666666" italic="true">
        Success demonstrated through templates and activities
      </note>
    </slide>

    <!-- Slide 6: Block 1 - Coaching Mindset -->
    <slide number="6" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 1: Coaching Mindset</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Coaching Mindset for Construction Managers
      </title>
      <content fontFamily="Arial" fontSize="18" color="#0033A0">
        <keyBeliefs>
          <belief icon="shield-check">Coaching supports on-site safety</belief>
          <belief icon="calendar">Enhances schedule adherence</belief>
          <belief icon="award">Improves quality outcomes</belief>
          <belief icon="trending-up">Builds team capability</belief>
        </keyBeliefs>
        <framework backgroundColor="#F5F5F5" padding="20px">
          <frameworkTitle fontSize="20" color="#D64309">Knowles' Adult Learning Principles</frameworkTitle>
          <principle>Self-direction: Adults want autonomy</principle>
          <principle>Relevance: Connect to real work challenges</principle>
          <principle>Practical application: Use it immediately</principle>
        </framework>
      </content>
      <image position="right" description="Manager coaching employee on construction site"/>
    </slide>

    <!-- Slide 7: Activity - Think-Pair-Share -->
    <slide number="7" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Reflect on Your Coaching Moments
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="users" size="48" color="#D64309"/>
        <prompt fontSize="22" color="#0033A0" bold="true">
          Identify a coaching moment you could have improved in your team
        </prompt>
        <steps fontSize="18" color="#0033A0">
          <step number="1">Individual reflection (1 minute)</step>
          <step number="2">Share 2 examples in your small group (4-6 people)</step>
          <step number="3">Select one example to refine using a coaching lens</step>
        </steps>
        <output backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <outputLabel fontSize="16" color="#D64309" bold="true">Output:</outputLabel>
          <outputText fontSize="18" color="#0033A0">
            Write 1 concise coaching question you could use next time
          </outputText>
        </output>
      </activityBox>
    </slide>

    <!-- Slide 8: Block 2 - 4-Step Model -->
    <slide number="8" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 2: The 4-Step Coaching Model</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Ask → Reflect → Decide → Commit
      </title>
      <processFlow>
        <step number="1" color="#0033A0" icon="help-circle">
          <stepTitle>ASK</stepTitle>
          <stepDescription>Gather facts, clarify the issue</stepDescription>
        </step>
        <arrow color="#D64309"/>
        <step number="2" color="#0033A0" icon="lightbulb">
          <stepTitle>REFLECT</stepTitle>
          <stepDescription>Explore options, consider constraints (safety, schedule, budget)</stepDescription>
        </step>
        <arrow color="#D64309"/>
        <step number="3" color="#0033A0" icon="target">
          <stepTitle>DECIDE</stepTitle>
          <stepDescription>Agree on a path (SMART goal)</stepDescription>
        </step>
        <arrow color="#D64309"/>
        <step number="4" color="#0033A0" icon="check-square">
          <stepTitle>COMMIT</stepTitle>
          <stepDescription>Define action steps and ownership</stepDescription>
        </step>
      </processFlow>
      <example backgroundColor="#F5F5F5" padding="15px">
        <exampleTitle fontSize="18" color="#D64309">Example: On-site misalignment</exampleTitle>
        <exampleText fontSize="16" color="#0033A0">
          Missed delivery window → Ask what happened → Reflect on prevention → Decide on notification system → Commit to implementation
        </exampleText>
      </example>
    </slide>

    <!-- Slide 9: Activity - Coaching Practice -->
    <slide number="9" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Practice the 4-Step Model
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="users-round" size="48" color="#D64309"/>
        <instructions fontSize="18" color="#0033A0">
          <instruction>Pair up: one person plays supervisor, the other a direct report</instruction>
          <instruction>Scenario: Missed delivery window or similar issue</instruction>
          <instruction>Use the fill-in-the-blank coaching script template</instruction>
          <instruction>Time: 8 minutes total</instruction>
        </instructions>
        <output backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <outputLabel fontSize="16" color="#D64309" bold="true">Deliverable:</outputLabel>
          <outputText fontSize="18" color="#0033A0">
            1-page coaching note capturing Ask, Reflect, Decide, Commit
          </outputText>
        </output>
      </activityBox>
    </slide>

    <!-- Slide 10: Block 3 - Demonstration -->
    <slide number="10" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 3: Coaching Demonstration</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Live Coaching Demonstration
      </title>
      <content fontFamily="Arial" fontSize="18" color="#0033A0">
        <demoSteps>
          <watchFor fontSize="20" color="#D64309" bold="true">Watch for these key techniques:</watchFor>
          <technique icon="ear">How to listen actively and rephrase</technique>
          <technique icon="messages">How to surface options without dictating</technique>
          <technique icon="handshake">How to close with a concrete commitment</technique>
        </demoSteps>
      </content>
      <scenarioBox backgroundColor="#F5F5F5" padding="20px" borderLeft="4px solid #D64309">
        <scenarioTitle fontSize="20" color="#0033A0" bold="true">On-Site Scenario:</scenarioTitle>
        <scenarioText fontSize="18" color="#0033A0">
          Team member struggling with quality standards on recent inspections
        </scenarioText>
      </scenarioBox>
      <image position="center" description="Two people in coaching conversation with hard hats"/>
    </slide>

    <!-- Slide 11: Activity - Role-Play Rotation -->
    <slide number="11" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Role-Play Rotation
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="repeat" size="48" color="#D64309"/>
        <instructions fontSize="18" color="#0033A0">
          <instruction bold="true">Switch roles: Practice both sides of the conversation</instruction>
          <instruction>Round 1: Partner A coaches Partner B (5 minutes)</instruction>
          <instruction>Round 2: Switch roles (5 minutes)</instruction>
        </instructions>
        <output backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <outputLabel fontSize="16" color="#D64309" bold="true">Outputs:</outputLabel>
          <outputItem>2 coaching scripts (one per person)</outputItem>
          <outputItem>1 clear SMART goal per script</outputItem>
          <outputItem>1 committed action with timeline</outputItem>
        </output>
      </activityBox>
    </slide>

    <!-- Slide 12: Block 4 - Psychological Safety -->
    <slide number="12" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 4: Psychological Safety</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Building Psychological Safety in Teams
      </title>
      <definition backgroundColor="#E6F0FF" padding="20px" borderLeft="4px solid #0033A0">
        <defTitle fontSize="20" color="#0033A0" bold="true">What is Psychological Safety?</defTitle>
        <defText fontSize="18" color="#0033A0">
          A climate where people feel safe to take risks, speak up, ask questions, and admit mistakes without fear of punishment or embarrassment
        </defText>
      </definition>
      <impact fontSize="18" color="#0033A0">
        <impactTitle fontSize="20" color="#D64309" bold="true">Impact on Construction Teams:</impactTitle>
        <impactItem icon="alert-triangle">Safety-critical decisions are surfaced earlier</impactItem>
        <impactItem icon="lightbulb">Creative problem-solving increases</impactItem>
        <impactItem icon="trending-up">Learning from mistakes improves quality</impactItem>
      </impact>
      <practices backgroundColor="#F5F5F5" padding="20px">
        <practiceTitle fontSize="20" color="#D64309">3 Practical Cues:</practiceTitle>
        <practice>1. PAUSE before deciding</practice>
        <practice>2. INVITE input from all voices</practice>
        <practice>3. APPRECIATE contributions publicly</practice>
      </practices>
    </slide>

    <!-- Slide 13: Activity - Micro-Trust Exercise -->
    <slide number="13" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Micro-Trust Exercise
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="heart-handshake" size="48" color="#D64309"/>
        <prompts fontSize="18" color="#0033A0">
          <promptTitle fontSize="20" color="#D64309" bold="true">Practice These Inclusive Behaviors:</promptTitle>
          <prompt number="1">"I'll pause and ask for your input before deciding."</prompt>
          <prompt number="2">"What concerns do you have about this approach?"</prompt>
          <prompt number="3">"Thank you for raising that—it's important we discuss it."</prompt>
        </prompts>
        <debrief backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <debriefTitle fontSize="16" color="#D64309" bold="true">Debrief Questions:</debriefTitle>
          <question>• What cues helped you feel safe?</question>
          <question>• What practice will you carry forward?</question>
        </debrief>
      </activityBox>
    </slide>

    <!-- Slide 14: Block 5 - Daily Huddles -->
    <slide number="14" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 5: Daily Huddles</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        15-Minute Daily Project Huddles
      </title>
      <purpose backgroundColor="#E6F0FF" padding="15px">
        <purposeTitle fontSize="20" color="#0033A0" bold="true">Purpose:</purposeTitle>
        <purposeText fontSize="18" color="#0033A0">
          Quick alignment, surface risks early, assign ownership, maintain momentum
        </purposeText>
      </purpose>
      <template backgroundColor="#F5F5F5" padding="20px">
        <templateTitle fontSize="20" color="#D64309" bold="true">6-Part Huddle Template:</templateTitle>
        <part number="1" time="1 min">START: Quick check-in</part>
        <part number="2" time="3 min">TOP PRIORITIES: What must get done today?</part>
        <part number="3" time="4 min">RISKS: What could derail us?</part>
        <part number="4" time="3 min">OWNERS: Who's responsible for what?</part>
        <part number="5" time="3 min">NEXT STEPS: Concrete actions with due dates</part>
        <part number="6" time="1 min">QUICK CLOSE: Recap and dismiss</part>
      </template>
      <image position="right" description="Team huddle on construction site"/>
    </slide>

    <!-- Slide 15: Activity - Design a Huddle -->
    <slide number="15" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Design Your 15-Minute Huddle
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="clipboard-check" size="48" color="#D64309"/>
        <instructions fontSize="18" color="#0033A0">
          <instruction bold="true">Create a huddle agenda for your current project</instruction>
          <instruction>Identify top 3 priorities for tomorrow</instruction>
          <instruction>List 3 potential risks and mitigation strategies</instruction>
          <instruction>Assign owners to each priority and risk</instruction>
        </instructions>
        <output backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <outputLabel fontSize="16" color="#D64309" bold="true">Deliverable:</outputLabel>
          <outputText fontSize="18" color="#0033A0">
            One-page huddle template with priorities, risks, and owners
          </outputText>
        </output>
      </activityBox>
    </slide>

    <!-- Slide 16: Block 6 - Role Clarity -->
    <slide number="16" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 6: Role Clarity & Team Health</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Roles, Responsibilities, and Collaboration
      </title>
      <framework backgroundColor="#F5F5F5" padding="20px">
        <frameworkTitle fontSize="20" color="#D64309" bold="true">Team Health Check Framework:</frameworkTitle>
        <dimension icon="target">CLARITY: Do we know our goals?</dimension>
        <dimension icon="check-circle">ACCOUNTABILITY: Do we own our work?</dimension>
        <dimension icon="users">COLLABORATION: Do we work well together?</dimension>
        <dimension icon="handshake">TRUST: Do we rely on each other?</dimension>
      </framework>
      <misalignment backgroundColor="#FFE5D9" padding="15px" borderLeft="4px solid #D64309">
        <misalignTitle fontSize="18" color="#D64309" bold="true">How Misalignment Shows Up:</misalignTitle>
        <sign>• Duplicated efforts</sign>
        <sign>• Missed handoffs</sign>
        <sign>• Unclear decision rights</sign>
        <sign>• Finger-pointing when issues arise</sign>
      </misalignment>
      <coachingRole fontSize="18" color="#0033A0">
        <roleTitle fontSize="20" color="#0033A0" bold="true">How Coaching Helps:</roleTitle>
        <roleText>Surface gaps, clarify expectations, agree on improvements</roleText>
      </coachingRole>
    </slide>

    <!-- Slide 17: Activity - Team Health Check -->
    <slide number="17" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Complete the Team Health Check
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="stethoscope" size="48" color="#D64309"/>
        <instructions fontSize="18" color="#0033A0">
          <instruction>Work in small groups (4-6 people)</instruction>
          <instruction>Rate your current team on each dimension (1-5 scale)</instruction>
          <instruction>Discuss: Where are the gaps?</instruction>
          <instruction>Identify at least ONE misalignment</instruction>
        </instructions>
        <output backgroundColor="#FFFFFF" borderColor="#0033A0" padding="15px">
          <outputLabel fontSize="16" color="#D64309" bold="true">Outputs:</outputLabel>
          <outputItem>Completed Team Health Check template</outputItem>
          <outputItem>One identified misalignment</outputItem>
          <outputItem>Two concrete actions to improve</outputItem>
        </output>
      </activityBox>
    </slide>

    <!-- Slide 18: Block 7 - Performance & Safety -->
    <slide number="18" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 7: Performance & Safety Coaching</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Coaching for Performance in Safety-Critical Contexts
      </title>
      <linkage backgroundColor="#E6F0FF" padding="20px">
        <linkageTitle fontSize="20" color="#0033A0" bold="true">Link Coaching to Core Outcomes:</linkageTitle>
        <link icon="shield">SAFETY: Prevent incidents through better communication</link>
        <link icon="award">QUALITY: Raise standards through feedback</link>
        <link icon="calendar">SCHEDULE: Keep projects on track through accountability</link>
      </linkage>
      <template backgroundColor="#F5F5F5" padding="20px" borderLeft="4px solid #D64309">
        <templateTitle fontSize="20" color="#D64309" bold="true">Performance Coaching Template:</templateTitle>
        <step>1. State the observation (specific, factual)</step>
        <step>2. Explain the impact (safety, quality, schedule)</step>
        <step>3. Ask for their perspective</step>
        <step>4. Agree on improvement actions</step>
        <step>5. Set check-in date</step>
      </template>
    </slide>

    <!-- Slide 19: Activity - Performance Role-Play -->
    <slide number="19" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Performance Coaching Role-Play
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="alert-triangle" size="48" color="#D64309"/>
        <scenario backgroundColor="#FFFFFF" padding="15px" borderColor="#0033A0">
          <scenarioTitle fontSize="20" color="#D64309" bold="true">Scenario:</scenarioTitle>
          <scenarioText fontSize="18" color="#0033A0">
            A team member's work quality has been slipping, and it now has safety implications. How do you coach them?
          </scenarioText>
        </scenario>
        <instructions fontSize="18" color="#0033A0">
          <instruction>Pair up and role-play the conversation</instruction>
          <instruction>Use the performance coaching template</instruction>
          <instruction>Time: 6 minutes (3 min conversation, 3 min debrief)</instruction>
        </instructions>
        <debrief fontSize="16" color="#0033A0">
          <debriefQ>• What felt effective?</debriefQ>
          <debriefQ>• What was challenging?</debriefQ>
        </debrief>
      </activityBox>
    </slide>

    <!-- Slide 20: Block 8 - Decision-Making & Conflict -->
    <slide number="20" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 8: Decision-Making & Conflict</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Decision-Making and Conflict Resolution Through Coaching
      </title>
      <techniques backgroundColor="#F5F5F5" padding="20px">
        <techniqueTitle fontSize="20" color="#D64309" bold="true">Key Techniques:</techniqueTitle>
        <technique icon="message-circle">Ask open questions to surface all perspectives</technique>
        <technique icon="scale">Acknowledge constraints (budget, timeline, safety)</technique>
        <technique icon="handshake">Guide toward shared decision</technique>
        <technique icon="arrow-down-circle">De-escalate tension by focusing on facts</technique>
      </techniques>
      <cues backgroundColor="#E6F0FF" padding="20px">
        <cueTitle fontSize="20" color="#0033A0" bold="true">Practical Coaching Cues:</cueTitle>
        <cue>"Help me understand your perspective..."</cue>
        <cue>"What constraints are we working within?"</cue>
        <cue>"What would a good outcome look like for both sides?"</cue>
        <cue>"What's one step we can agree on right now?"</cue>
      </cues>
    </slide>

    <!-- Slide 21: Activity - Conflict Resolution -->
    <slide number="21" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Conflict-Resolution Role-Play
      </title>
      <activityBox backgroundColor="#FFE5D9" borderColor="#D64309" padding="30px">
        <icon name="users-round" size="48" color="#D64309"/>
        <scenario backgroundColor="#FFFFFF" padding="15px" borderColor="#0033A0">
          <scenarioTitle fontSize="20" color="#D64309" bold="true">Scenario:</scenarioTitle>
          <scenarioText fontSize="18" color="#0033A0">
            Two team members disagree on resource allocation for competing priorities. Tensions are rising.
          </scenarioText>
        </scenario>
        <instructions fontSize="18" color="#0033A0">
          <instruction>Groups of 3: One coach, two team members in conflict</instruction>
          <instruction>Use coaching questions to move toward shared decision</instruction>
          <instruction>Time: 8 minutes</instruction>
        </instructions>
        <debrief fontSize="16" color="#0033A0">
          <debriefTitle bold="true">Reflect:</debriefTitle>
          <debriefQ>• What helped de-escalate the situation?</debriefQ>
          <debriefQ>• What will you use in your real work?</debriefQ>
        </debrief>
      </activityBox>
    </slide>

    <!-- Slide 22: Block 9 - Project Lifecycle Integration -->
    <slide number="22" layout="content">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <sectionHeader backgroundColor="#0033A0" textColor="#FFFFFF">Block 9: Integrating Coaching</sectionHeader>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Embedding Coaching in the Project Lifecycle
      </title>
      <lifecycle backgroundColor="#F5F5F5" padding="20px">
        <lifecycleTitle fontSize="20" color="#D64309" bold="true">Key Coaching Moments:</lifecycleTitle>
        <phase icon="rocket">PLANNING/KICKOFF: Set expectations, clarify roles</phase>
        <phase icon="flag">MILESTONES: Check progress, adjust course</phase>
        <phase icon="trending-up">EXECUTION: Daily huddles, real-time problem-solving</phase>
        <phase icon="clipboard-check">POST-MORTEM: Reflect, learn, improve for next time</phase>
      </lifecycle>
      <guidance backgroundColor="#E6F0FF" padding="20px">
        <guidanceTitle fontSize="20" color="#0033A0" bold="true">When to Coach vs. When to Escalate:</guidanceTitle>
        <coachWhen fontSize="18" color="#0033A0">
          <label bold="true">Coach when:</label> Development opportunity, capability gap, motivation issue
        </coachWhen>
        <escalateWhen fontSize="18" color="#D64309">
          <label bold="true">Escalate when:</label> Policy violation, repeated performance failure, safety emergency
        </escalateWhen>
      </guidance>
    </slide>

    <!-- Slide 23: Activity - Integration Action Plan -->
    <slide number="23" layout="activity">
      <orangeBar position="left" width="20px" color="#D64309"/>
      <title fontFamily="Arial" fontSize="32" color="#0033A0">
        Activity: Embed