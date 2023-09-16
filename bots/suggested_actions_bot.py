
from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions

class SuggestActionsBot(ActivityHandler):
    def __init__(self):
        self.conversation_state = {}

    async def on_members_added_activity(
            self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()

        if text == "start over":
            # Clear conversation state to restart
            self.conversation_state.clear()
            await self._send_welcome_message(turn_context)
        elif 'state' in self.conversation_state:
            # Handle subtopics based on conversation state
            if self.conversation_state['state'] == 'website_development':
                response_text, is_leaf_node = self._process_website_development_input(text)
            elif self.conversation_state['state'] == 'mobile_app_development':
                response_text, is_leaf_node = self._process_mobile_app_development_input(text)
            elif self.conversation_state['state'] == 'competitive_programming':
                response_text, is_leaf_node = self._process_competitive_programming_input(text)
            else:
                response_text = "Please select one of the available options."

            if is_leaf_node:
                await turn_context.send_activity(MessageFactory.text(response_text))
            else:
                await self._send_suggested_actions(turn_context, response_text)
        else:
            response_text = self._process_input(text)
            await turn_context.send_activity(MessageFactory.text(response_text))

            if text == "website development":
                self.conversation_state['state'] = 'website_development'
                await self._send_website_development_actions(turn_context)
            elif text == "mobile app development":
                self.conversation_state['state'] = 'mobile_app_development'
                await self._send_mobile_app_development_actions(turn_context)
            elif text == "competitive programming":
                self.conversation_state['state'] = 'competitive_programming'
                await self._send_competitive_programming_actions(turn_context)
            else:
                await self._send_suggested_actions(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        welcome_message = (
            "Hi, I'm the Tech Resources Bot. I can help you explore different topics:"
        )
        await turn_context.send_activity(MessageFactory.text(welcome_message))
        await self._send_suggested_actions(turn_context)

    def _process_input(self, text: str):
        if text == "website development":
            return "Great choice! Let's explore Website Development."
        if text == "mobile app development":
            return "Sure! Let's dive into Mobile App Development."
        if text == "competitive programming":
            return "Excellent! Let's get started with Competitive Programming."
        return "Please select one of the available options."

    def _process_website_development_input(self, text: str):
        if text == "frontend development":
            return "Frontend Development involves creating the user interface and user experience of a website. It includes HTML, CSS, and JavaScript.", True
        if text == "backend development":
            return "Backend Development involves server-side programming and database management to make websites functional.", True
        if text == "ui/ux":
            return "UI/UX stands for User Interface (UI) and User Experience (UX) design, focusing on making websites user-friendly and visually appealing.", True
        return "What aspect of Website Development are you interested in?", False

    def _process_mobile_app_development_input(self, text: str):
        if text == "android app development":
            return "Android App Development involves creating mobile applications specifically for Android devices using Java or Kotlin.", True
        if text == "ios app development":
            return "iOS App Development focuses on creating mobile applications for Apple's iOS devices using Swift or Objective-C.", True
        return "What aspect of Mobile App Development are you interested in?", False

    def _process_competitive_programming_input(self, text: str):
        if text == "algorithm challenges":
            return "Algorithm Challenges involve solving complex coding problems and optimizing algorithms.", True
        if text == "online coding platforms":
            return "Online Coding Platforms provide a platform for practicing coding challenges and participating in coding competitions.", True
        return "What aspect of Competitive Programming are you interested in?", False

    async def _send_suggested_actions(self, turn_context: TurnContext, prompt=None):
        actions = [
            CardAction(
                title="Website Development",
                type=ActionTypes.im_back,
                value="Website Development",
            ),
            CardAction(
                title="Mobile App Development",
                type=ActionTypes.im_back,
                value="Mobile App Development",
            ),
            CardAction(
                title="Competitive Programming",
                type=ActionTypes.im_back,
                value="Competitive Programming",
            ),
            CardAction(  # Adding the "Start Over" option
                title="Start Over",
                type=ActionTypes.im_back,
                value="Start Over",
            ),
        ]

        reply = MessageFactory.text(prompt or "What would you like to explore?")
        reply.suggested_actions = SuggestedActions(actions=actions)
        await turn_context.send_activity(reply)

    async def _send_website_development_actions(self, turn_context: TurnContext):
        actions = [
            CardAction(
                title="Frontend Development",
                type=ActionTypes.im_back,
                value="Frontend Development",
            ),
            CardAction(
                title="Backend Development",
                type=ActionTypes.im_back,
                value="Backend Development",
            ),
            CardAction(
                title="UI/UX",
                type=ActionTypes.im_back,
                value="UI/UX",
            ),
            CardAction(  # Adding the "Start Over" option
                title="Start Over",
                type=ActionTypes.im_back,
                value="Start Over",
            ),
        ]

        reply = MessageFactory.text("What aspect of Website Development are you interested in?")
        reply.suggested_actions = SuggestedActions(actions=actions)
        await turn_context.send_activity(reply)

    async def _send_mobile_app_development_actions(self, turn_context: TurnContext):
        actions = [
            CardAction(
                title="Android App Development",
                type=ActionTypes.im_back,
                value="Android App Development",
            ),
            CardAction(
                title="iOS App Development",
                type=ActionTypes.im_back,
                value="iOS App Development",
            ),
            CardAction(  # Adding the "Start Over" option
                title="Start Over",
                type=ActionTypes.im_back,
                value="Start Over",
            ),
        ]

        reply = MessageFactory.text("What aspect of Mobile App Development are you interested in?")
        reply.suggested_actions = SuggestedActions(actions=actions)
        await turn_context.send_activity(reply)

    async def _send_competitive_programming_actions(self, turn_context: TurnContext):
        actions = [
            CardAction(
                title="Algorithm Challenges",
                type=ActionTypes.im_back,
                value="Algorithm Challenges",
            ),
            CardAction(
                title="Online Coding Platforms",
                type=ActionTypes.im_back,
                value="Online Coding Platforms",
            ),
            CardAction(  # Adding the "Start Over" option
                title="Start Over",
                type=ActionTypes.im_back,
                value="Start Over",
            ),
        ]

        reply = MessageFactory.text("What aspect of Competitive Programming are you interested in?")
        reply.suggested_actions = SuggestedActions(actions=actions)
        await turn_context.send_activity(reply)
