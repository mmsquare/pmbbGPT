// Product Management Training Data for Few-Shot Learning
const TRAINING_DATA = [
    {
        "input": "How should I prioritize these features when everything feels urgent?",
        "output": "Prioritization is only possible when project's goal and target audience are clearly defined. e.g. if the project's first milestone's goal is to validate whether users find beauty product review content useful, we should focus our energy on curating list of most useful content we can find and show users directly. Meanwhile, we should skip features such as login, account creation and likes."
    },
    {
        "input": "What's the best way to define a product strategy for a new 0→1 product?",
        "output": "a strategy is a statement of how we can win a target segment by poviding values that we are in a unique position to offer. Therefore, I would follow up with more questions: who's your target audience, what problem you are tryhing to solve, what unique value are you offering to solve the problem, is it defensible, how are you going to validate your value hypothesis quickly withtout even building a product"
    },
    {
        "input": "The founder wants to build X, but it doesn't align with user needs. What should I do?",
        "output": "Ask clarificaitons questions: what problem are you trying to solve by building this feature. If we solve the problem, what's the ideal outcome. If the feature really does not align with users' need, it's obvious that the problem we are solving is not the right one or the solution could be better. More often than not, there are founder/manager/boss who have some intuiation on what to build but not able to articulate very well the user problem, as a product person, instead of having a prolonged argument over opinions or semi-supported points, we should try to help them write down the best answers right now and validate with more evidence in the future. Writing them down help everyone on the team clear why we do something and validate once we have some results, validate and improve our decision making next time."
    },
    {
        "input": "How do I make tradeoffs between growth and retention?",
        "output": "Retention is usually meansurement of user experience and level of product-market-fit. Growth measures a product's market take-over speed and demonstrate real-world impact. Short answer is that, we should always care retention more than growth unless growth itself can bring a network effect that improves user experience and retention. In reality, it really depends on the situation the product is currently operating under. If the project has good-enough retention and also under pressure to take over market share, growth is prioritized; if retention is not good enough, we might need to improve the user experience and add user value or look for new growth channel to improe user retention before growing."
    },
    {
        "input": "We're in a crowded market. How do we differentiate our product strategy?",
        "output": "a good strategy is where we do things that we are unique position to do well that is impossible or dificult to be picked up by competitors. If we already have initial tractions, I'll ask ourselves what makes our product unique that user chooses us over competitors and double-down on that. If we do not yet have initial user base, i'll think about a few hypothesis that if we do well, we will provide a unique value to the users that our team has strength to do well and maintain."
    }
];

module.exports = TRAINING_DATA;