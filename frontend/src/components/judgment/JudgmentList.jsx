import JudgmentCard from "./JudgmentCard";

function JudgmentList({

    judgments,

    onExplain,

    onOpen,

    onRelevant

}) {

    if (!judgments || judgments.length === 0) {

        return (

            <div className="judgment-sidebar-empty">

                <h2>Relevant Judgments</h2>

                <p>No judgments yet.</p>

            </div>

        );

    }

    return (

        <div className="judgment-sidebar">

            <h2>Relevant Judgments</h2>

            {

                judgments.map((judgment, index) => (

                    <JudgmentCard

                        key={index}

                        judgment={judgment}

                        onExplain={onExplain}

                        onOpen={onOpen}

                        onRelevant={onRelevant}

                    />

                ))

            }

        </div>

    );

}

export default JudgmentList;