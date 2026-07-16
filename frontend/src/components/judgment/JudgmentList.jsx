import JudgmentCard from "./JudgmentCard";

function JudgmentList({ results }) {

    return (

        <div>

            {results.map((judgment, index) => (

                <JudgmentCard

                    key={index}

                    judgment={judgment}

                />

            ))}

        </div>

    );

}

export default JudgmentList;