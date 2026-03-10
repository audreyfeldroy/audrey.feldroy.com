# Cookiecutter, Chardet, and the Cascade

Lately I've been catching up on open source. This is the backstory behind the Cookiecutter release cascade. One quick release turned into four all-consuming releases, a licensing dispute, chardet removal, a new decision tree classifier in binaryornot, and my new interest in becoming an expert at designing classifiers.

## The Myth of the Quick Release

Putting out Cookiecutter 2.7.0 meant that I had to scramble to patch something. Then I put out a 2.7.1 release. Then I discovered Cookiecutter was outputting a warning about chardet versions. 

The root cause of that warning was dependency binaryornot using chardet < 7. When I looked into updating its chardet version, I discovered it wasn't as easy as changing a number. There was a licensing dispute in chardet 7 that I had to carefully consider.

What no one talks about is how doing a release on a large open source project basically turns into a full-time commitment for the next week as you rush to put out fixes. I'm grateful to [Daniel Roy Greenfeld](https://daniel.feldroy.com) for the extra time he put in watching our daughter, and for his patience with me putting work on hold for all this.

## The Licensing Situation

Back to what happened with binaryornot and chardet. I saw a really promising rewrite in 7.0.0 that had been implemented with AI assistance. I was eager to try it out. But the maintainer had changed the license without the author’s consent, and the author disputed it. I saw valid arguments for both sides, didn't want to get involved, and even tried an alternative before I decided just removing it was the simplest path.

## Ultimate Considerations

In the end what matters to me is:

1) The real users of Cookiecutter and binaryornot. That they have great experiences with my FOSS projects and don’t have to stress over licenses.

2) My enjoyment, well-being, and peace of mind. Open source is volunteer work for me. It has to be fun or I’ll just stop. (Using AI to improve my code, teach myself new things, and handle tedious parts like writing great commit messages is a part of that fun, btw.)

3) Respect for those around me in the ecosystem. This includes the upstream creator and maintainers of chardet, and all the downstream package creators and maintainers who use binaryornot and Cookiecutter.

## Removal of Chardet, and Dependency Minimization

I decided to remove chardet from binaryornot and therefore from Cookiecutter. For now. It may come back, or I may bring in an alternative. In place of chardet, binaryornot now uses a decision tree classifier that I used scikit-learn to generate. 

I would have used another classifier type but wanted zero dependencies, out of consideration for downstream maintainers. 

## Belt-and-Suspenders Classifying

The classifier in binaryornot 0.5.0 had mistakes in it. I fixed them as best I could, though I knew it still needed work. I decided to take a belt-and-suspenders approach, putting in guardrails before the decision tree is even reached. That required checking file extensions and magic signatures. It was enough of a change that my goal of a 0.5.1 patch turned into 0.6.0.

## Improving the Classifier

I’m not an expert at encodings or classifiers. Yet. 

(When I wrote Cookiecutter I was also not an expert on project templating. Now I am. I’m doing almost-unimaginable things with Cookiecutter. I’ll share those soon.)

Anyhow my next step with binaryornot is to improve the classifier to the point that I feel comfortable updating the binaryornot version in Cookiecutter.

## Call for Expert Help

If you’re an expert on building great classifiers, I’d love to pair program with you over screenshare. I’m flexible with working in notebooks, editing code directly, or using agentic AI as long as we micromanage its generated output together. Maybe we can even test-drive [hamelnb](https://github.com/hamelsmu/hamelnb) or other fun new tools together.

You’ll be credited for your work thoughtfully in my release notes and beyond.

Tags: cookiecutter, binaryornot, open-source