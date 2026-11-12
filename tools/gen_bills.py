# Generates the bills: the per-bill events (source/scenes/parliament/bills.scene.dry)
# and the shared definitions (source/scenes/parliament/bill_defs.scene.dry).
# Edit the BILLS list below, then run from the repository root:
#     python3 tools/gen_bills.py .
# A new bill also needs a card option that introduces it (see the Housing card's
# right_to_buy option): set bill_new = "<key>" and call bill_introduce.
import json, os, sys

repo = sys.argv[1]
out_dir = os.path.join(repo, 'source/scenes/parliament')
os.makedirs(out_dir, exist_ok=True)

FACTION_NAME = {'wet': 'the wets', 'dry': 'the dries', 'right': 'the right', 'loyalist': 'the loyalists'}

BILLS = [
    dict(
        key='employment1', name='Employment Bill', act='Employment Act',
        faction='right', weight=0.25, champion='dry', committee=2, lords=1, amend=0.35, lords_risk=0.12,
        lib='abstain', ulster='abstain',
        second="""[+ employment_secretary +]'s Employment Bill limits lawful picketing to a worker's own place of work, protects workers who refuse to join a closed shop on grounds of conscience, and offers public money for postal ballots. Labour calls it an attack on the whole trade union movement. A few of our own backbenchers say it doesn't go nearly far enough.""",
        amend_title='In Committee: the Employment Bill',
        amend_text="""Backbenchers on the right have tabled amendments to ban the closed shop outright and to make unions liable for damages from secondary action. [+ employment_secretary +] says the amendments would wreck the bill and unite the unions against it.""",
        amend_yes=('Accept the amendments and toughen the bill.', 'Union power falls further. The wets and the TUC are furious.',
                   'right_dissent -= 3; dry_dissent -= 2; wet_dissent += 4; bill_employment1_tough = 1',
                   'The bill comes back from committee with teeth. The TUC General Council calls an emergency meeting.'),
        amend_no=('Keep the bill as it is.', 'The right grumbles. Step by step was the plan.',
                  'right_dissent += 3; dry_dissent += 2',
                  'The amendments are voted down in committee, with the whips making sure the right-wingers on the committee are outnumbered.'),
        lords_title='The Lords Amend the Employment Bill',
        lords_text="""The House of Lords votes to widen the conscience clause, so that anyone with a deeply held personal objection to joining a union is protected from dismissal from a closed shop.""",
        lords_yes=('Accept the Lords amendment.', 'A small win for the right.',
                   'right_dissent -= 2; wet_dissent += 1',
                   'The government accepts the amendment. Union leaders say the closed shop is being dismantled one clause at a time.'),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'right_dissent += 2; wet_dissent -= 1'),
        law="""union_power -= 10; union_power -= 4 if bill_employment1_tough = 1; employment_acts += 1; strike_wave += 0.5; c2_con += 1*(1-dissent) if union_backlash >= 60""",
        law_text="""The Employment Act [+ year +] receives Royal Assent. Pickets must now stay at their own place of work, new closed shops need the support of four workers in five in a secret ballot, and public money pays for postal ballots.[? if bill_employment1_tough = 1 : The amendments from the right mean that unions can now be sued for damages from secondary action. ?]""",
        achievement=None),
    dict(
        key='employment2', name='Employment Bill', act='Employment Act',
        faction='wet', weight=0.5, champion='dry', committee=2, lords=1, amend=0.4, lords_risk=0.15,
        lib='no', ulster='abstain',
        second="""The second Employment Bill removes the blanket immunity that has protected union funds since 1906. A union that calls an unlawful strike will put its money at risk, the definition of a lawful trade dispute is narrowed, and every closed shop must win a large majority in a secret ballot. Union leaders say it is the worst attack on their rights since the General Strike, and some of our own wets agree with them in private.""",
        amend_title='In Committee: the Employment Bill',
        amend_text="""Wets on the standing committee want to drop the clause that exposes union funds to damages, leaving the liability with individual officials. They say a union whose funds are seized will become a union of martyrs.""",
        amend_yes=('Accept the amendment.', 'The bill is weaker. The wets are soothed; the dries are not.',
                   'wet_dissent -= 3; dry_dissent += 4; bill_employment2_watered = 1',
                   'The clause goes. The unions are relieved, and the dries mutter that the government has lost its nerve.'),
        amend_no=('Reject it.', 'The wets will not forget it.',
                  'wet_dissent += 3; dry_dissent -= 2; rebellion += 0.3',
                  'The committee votes the amendment down by a single vote, after the whips change two of its members overnight.'),
        lords_title='The Lords Amend the Employment Bill',
        lords_text="""The House of Lords votes to hold closed-shop ballots every ten years instead of every five, which would leave most existing closed shops undisturbed for a decade.""",
        lords_yes=('Accept the Lords amendment.', 'Union power falls a little less.',
                   'wet_dissent -= 2; dry_dissent += 2; bill_employment2_watered = 1',
                   'The government gives way. The bill is still the toughest union law for half a century.'),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'dry_dissent -= 2; wet_dissent += 2'),
        law="""union_power -= 20; union_power += 7 if bill_employment2_watered = 1; employment_acts += 1; strike_wave += 1.5; c2_con += 2*(1-dissent) if union_backlash >= 60; c2_lab += 1 if union_backlash < 60""",
        law_text="""The Employment Act [+ year +] receives Royal Assent. [? if bill_employment2_watered = 0 : A union that calls an unlawful strike now risks its funds, and the courts can seize them. ?][? if bill_employment2_watered = 1 : Unions that call unlawful strikes face the courts, though the bill has lost some of its sharpest edges on the way. ?] The unions' long immunity from the law is over.""",
        achievement=None),
    dict(
        key='trade_union', name='Trade Union Bill', act='Trade Union Act',
        faction='wet', weight=0.15, champion='dry', committee=2, lords=1, amend=0.4, lords_risk=0.2,
        lib='yes', ulster='abstain',
        second="""The Trade Union Bill gives members the final say. A strike called without a secret ballot loses its legal immunity, union executives must face a secret ballot of the members every five years, and every ten years members must vote on whether their union keeps a political fund, the money that pays for the Labour Party.""",
        amend_title='In Committee: the Trade Union Bill',
        amend_text="""Backbenchers want to go further and make union members opt in to paying the political levy, instead of having to opt out. It would cut off much of the Labour Party's money. The TUC has offered a deal: if the government drops the idea, unions will tell every member of the right to opt out.""",
        amend_yes=('Make members opt in to the levy.', "Labour's finances suffer. The wets call it partisan.",
                   'dry_dissent -= 3; right_dissent -= 2; wet_dissent += 4; bill_trade_union_tough = 1',
                   'The amendment is carried. Labour says the Conservatives are trying to bankrupt the opposition; the party treasurer at Central Office says nothing at all.'),
        amend_no=("Take the TUC's deal.", 'The bill passes more smoothly. The dries are disappointed.',
                  'dry_dissent += 2; wet_dissent -= 2; union_power -= 1',
                  'The deal is done at the Department of Employment. The unions will write to their members about opting out, and the government will leave the levy alone.'),
        lords_title='The Lords Amend the Trade Union Bill',
        lords_text="""Peers led by former Labour ministers vote to let unions hold strike ballots at the workplace, by a show of hands in a secret booth if need be, rather than by post.""",
        lords_yes=('Accept the Lords amendment.', 'Workplace ballots are easier to win for the militants.',
                   'wet_dissent -= 1; dry_dissent += 2; bill_trade_union_watered = 1',
                   'The government accepts workplace ballots as an alternative to the post.'),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'dry_dissent -= 1; wet_dissent += 1'),
        law="""union_power -= 10; union_power += 3 if bill_trade_union_watered = 1; strike_wave -= 1; c2_con += 1*(1-dissent); labour_credibility -= 4 if bill_trade_union_tough = 1; lab_leader_rating -= 2 if bill_trade_union_tough = 1""",
        law_text="""The Trade Union Act [+ year +] receives Royal Assent. From now on, no ballot means no immunity. Moderates expect to win more union elections; the militants expect to win more strike ballots. Both are about to find out.""",
        achievement=None),
    dict(
        key='housing', name='Housing Bill', act='Housing Act',
        faction='wet', weight=0.12, champion='dry', committee=3, lords=2, amend=0.4, lords_risk=0.5,
        lib='abstain', ulster='abstain',
        second="""The Housing Bill gives every council tenant of three years' standing the right to buy their home, at a discount of a third rising to a half of its value, and the right to a council mortgage if the building society says no. Labour councils say they will refuse to sell. The bill says they won't have the choice.""",
        amend_title='In Committee: the Housing Bill',
        amend_text="""Members for rural and seaside seats want councils in National Parks and Areas of Outstanding Natural Beauty to be able to stop former council houses being sold on as holiday cottages.""",
        amend_yes=('Accept the amendment.', 'The shires are content.',
                   'wet_dissent -= 2; dry_dissent += 1',
                   'Councils in the National Parks may now attach a covenant, so that a house bought under the right to buy can only be resold to someone who lives or works locally.'),
        amend_no=('Reject it.', 'A few county members will rebel.',
                  'wet_dissent += 2; rebellion += 0.3',
                  "The amendment is defeated. The Lake District's member says the cottages will be full of weekenders from Manchester by 1985."),
        lords_title='The Lords Amend the Housing Bill',
        lords_text="""The House of Lords votes to exempt sheltered housing built for the elderly from the right to buy. Peers on all sides say councils that sell their old people's bungalows will never be able to replace them.""",
        lords_yes=('Accept the Lords amendment.', 'The wets approve. The right to buy is little changed.',
                   'wet_dissent -= 2; right_dissent += 1',
                   'The government accepts that housing designed for the elderly should be kept for them.'),
        lords_no=('Overturn it in the Commons.', 'Headlines about selling pensioners\' homes. The Lords may back down.',
                  'thatcher_rating -= 1; wet_dissent += 2; dry_dissent -= 1'),
        law="""right_to_buy_progress += 1; budget += 1; budget -= 0.5 if bill_housing_watered = 1; c2_con += 2*(1-dissent); de_con += 2*(1-dissent); policy_right_to_buy = 1""",
        law_text="""The Housing Act [+ year +] receives Royal Assent. Within weeks, the town halls are swamped with application forms. Families who never expected to own anything are measuring up for new front doors, the first thing many of them change.""",
        achievement=None),
    dict(
        key='education', name='Education Bill', act='Education Act',
        faction='wet', weight=0.1, champion='dry', committee=2, lords=2, amend=0.3, lords_risk=0.65,
        lib='abstain', ulster='abstain',
        second="""The Education Bill gives parents the right to state a preference for their child's school, a place on every governing body, and the right to see each school's exam results. It also lets councils charge for school buses, and ends the duty to provide school milk and a school dinner at a fixed price.""",
        amend_title='In Committee: the Education Bill',
        amend_text="""Backbenchers want to keep a minimum standard for school dinners, so that councils can't replace them with a bun and a bag of crisps.""",
        amend_yes=('Accept the amendment.', '-0.3 budget. The wets approve.',
                   'budget -= 0.3; wet_dissent -= 2; dry_dissent += 1',
                   'The nutritional standards stay. The Treasury says it is the most expensive bun in history.'),
        amend_no=('Reject it.', 'Councils will have a free hand.',
                  'wet_dissent += 2; rebellion += 0.2',
                  'The amendment falls. In a year, the school canteen will be selling chips.'),
        lords_title='The Lords Rebel',
        lords_text="""The bill would let councils charge for school buses. In the House of Lords, the Duke of Norfolk leads Conservative peers, many of them from rural counties with Catholic schools miles from home, in a rebellion. The clause is defeated by a large majority.""",
        lords_yes=('Accept the defeat and drop the charges.', '-0.3 budget. The shires are relieved.',
                   'budget -= 0.3; wet_dissent -= 2; dry_dissent += 1; loyalist_dissent -= 1',
                   'The charges are dropped. The Lords have shown that they can still embarrass a government with a working majority.'),
        lords_no=('Overturn the Lords in the Commons.', '+0.5 budget if it works. Backbenchers from rural seats will rebel.',
                  'rebellion += 1; wet_dissent += 3; c2_con -= 1'),
        law="""parental_choice = 1; c1_con += 2*(1-dissent); c1_con -= 1 if bill_education_watered = 1; c2_con += 1*(1-dissent); budget += 0.5 if bill_education_insisted = 1""",
        law_text="""The Education Act [+ year +] receives Royal Assent. Parents can now say which school they want and read its exam results. The councils that planned their catchment areas street by street have to start again.""",
        achievement=None),
    dict(
        key='nationality', name='British Nationality Bill', act='British Nationality Act',
        faction='wet', weight=0.45, champion='right', committee=3, lords=2, amend=0.4, lords_risk=0.5,
        lib='no', ulster='yes',
        second="""The British Nationality Bill replaces citizenship of the United Kingdom and Colonies with three categories: British citizenship, British Dependent Territories citizenship and British Overseas citizenship. Only the first carries the right to live here, and a child born in Britain will no longer be British by birth alone unless a parent is settled here. The bishops, the Liberals and the Commission for Racial Equality are against it.""",
        amend_title='In Committee: the British Nationality Bill',
        amend_text="""Wets on the committee want any child born here who lives here for their first ten years to have the right to register as a British citizen, whatever their parents' status.""",
        amend_yes=('Accept the amendment.', 'The wets are soothed. The right is not.',
                   'wet_dissent -= 3; right_dissent += 2',
                   'The ten-year rule goes into the bill. The Home Office calculates that it will affect a few hundred children a year.'),
        amend_no=('Reject it.', 'The wets dig in.',
                  'wet_dissent += 3; right_dissent -= 1; rebellion += 0.3',
                  'The amendment is defeated after a long night in committee.'),
        lords_title='The Lords Amend the British Nationality Bill',
        lords_text="""The House of Lords votes to give the people of Gibraltar full British citizenship, against the government's advice. The Foreign Office warns that Spain is watching, and that Hong Kong will ask why the Rock deserves what it does not.""",
        lords_yes=('Accept the Lords amendment.', 'The right is pleased. Madrid is not.',
                   'right_dissent -= 2; europe_relation -= 1',
                   'The government gives way. Gibraltar celebrates; the Spanish foreign ministry issues a statement.'),
        lords_no=('Overturn it in the Commons.', 'The right objects. The Lords may back down.',
                  'right_dissent += 3; wet_dissent -= 1'),
        law="""nationality_act = 1; right_strength += 2; right_dissent += 3 if bill_nationality_watered = 1; c2_con += 1*(1-dissent); lib_relation -= 2""",
        law_text="""The British Nationality Act [+ year +] receives Royal Assent. Only British citizens now have the automatic right to live here. Critics say the Act was designed to keep people out, and in Hong Kong three million people discover that their passports no longer mean what they thought.""",
        achievement='nationality'),
    dict(
        key='rates', name='Rates Bill', act='Rates Act',
        faction='wet', weight=0.8, champion='right', committee=3, lords=2, amend=0.4, lords_risk=0.35,
        lib='no', ulster='abstain',
        second="""The Rates Bill gives [+ environment_secretary +] the power to set a maximum rate for any council that overspends, and a reserve power to cap every council in the country. Ted Heath leads the backbench opposition, and Labour councils in Liverpool and Lambeth say they will defy the law.""",
        amend_title='In Committee: the Rates Bill',
        amend_text="""Wets want the general power to cap every council in the country dropped, leaving only the selective scheme for the worst overspenders.""",
        amend_yes=('Accept the amendment.', 'The wets are soothed. Ratepayers get less relief.',
                   'wet_dissent -= 3; right_dissent += 2; bill_rates_watered = 1',
                   'The general power goes. Only the councils named each year by the Environment Secretary will be capped.'),
        amend_no=('Reject it.', 'The wets dig in.',
                  'wet_dissent += 3; right_dissent -= 1; rebellion += 0.5',
                  'The amendment is defeated. The county councils, many of them Conservative, start to worry.'),
        lords_title='The Lords Amend the Rates Bill',
        lords_text="""The House of Lords votes to make the Environment Secretary consult each council before capping its rate, and to let councils appeal.""",
        lords_yes=('Accept the Lords amendment.', 'A delay in each case, nothing worse.',
                   'wet_dissent -= 2',
                   'The government accepts the duty to consult. Councils will be able to make their case before the cap comes down.'),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'wet_dissent += 2; right_dissent -= 1'),
        law="""rate_capping = 1; c1_con += 2*(1-dissent); c1_con -= 1 if bill_rates_watered = 1; ab_con += 1*(1-dissent); right_dissent -= 2""",
        law_text="""The Rates Act [+ year +] receives Royal Assent. For the first time, Whitehall can tell an elected council how much it may raise. Ratepayers in the overspending boroughs cheer; the councils in Liverpool and Lambeth start planning a budget they cannot legally set.""",
        achievement=None),
    dict(
        key='glc', name='Local Government Bill', act='Local Government Act',
        faction='wet', weight=1.0, champion='right', committee=2, lords=2, amend=0.4, lords_risk=0.7,
        lib='no', ulster='abstain',
        second="""The Local Government Bill abolishes the Greater London Council and the six metropolitan counties, and cancels next year's elections to them, handing their work to appointed boards in the meantime. Ken Livingstone's campaign has covered London with posters that say "Say No to No Say", and his popularity has never been higher.""",
        amend_title='In Committee: the Local Government Bill',
        amend_text="""London Conservatives want a new elected body to run the capital's strategic services, its roads, its fire brigade and its planning, once the GLC is gone.""",
        amend_yes=('Accept the amendment.', 'The wets approve. The right asks what the point was.',
                   'wet_dissent -= 3; right_dissent += 3; bill_glc_watered = 1',
                   'London will get a smaller, elected strategic authority in place of the GLC. Livingstone says he will stand for it.'),
        amend_no=('Reject it.', 'London Tories will rebel.',
                  'wet_dissent += 3; right_dissent -= 2; rebellion += 0.5',
                  "The amendment is defeated. London's services will be run by joint boards of the boroughs."),
        lords_title='The Lords Defeat the Local Government Bill',
        lords_text="""The House of Lords votes down the plan to cancel next year's elections and replace the councillors with nominees. Peers of every party say it is wrong to abolish an election before Parliament has abolished the council.""",
        lords_yes=('Let the councillors serve on until abolition.', 'Livingstone stays at County Hall a little longer.',
                   'wet_dissent -= 2; thatcher_rating -= 1',
                   'The government gives way. The councillors elected in 1981 will serve until the council disappears, and Livingstone gets another year on the roof of County Hall.'),
        lords_no=('Overturn the Lords in the Commons.', 'The rebellion grows. The Lords may back down.',
                  'rebellion += 1; wet_dissent += 3; c1_con -= 1'),
        law="""glc_abolition = 1; c1_con += 1*(1-dissent); right_dissent -= 2; right_dissent += 3 if bill_glc_watered = 1""",
        law_text="""The Local Government Act [+ year +] receives Royal Assent. The Greater London Council and the metropolitan counties will be gone within two years.[? if bill_glc_watered = 1 : A smaller elected authority will look after London's roads and planning. ?] Across the river, the unemployment figures on the roof of County Hall are updated as usual.""",
        achievement='glc'),
    dict(
        key='pace', name='Police and Criminal Evidence Bill', act='Police and Criminal Evidence Act',
        faction='wet', weight=0.2, champion='right', committee=3, lords=2, amend=0.5, lords_risk=0.4,
        lib='no', ulster='yes',
        second="""The Police and Criminal Evidence Bill puts the powers of stop, search, arrest and detention into a single code, with new safeguards for suspects: time limits on detention, a custody officer at every station, and a record of every search. The police say it ties their hands. Doctors, priests and journalists say the new powers to search for evidence would let the police into their confidential files.""",
        amend_title='In Committee: the Police and Criminal Evidence Bill',
        amend_text="""Backbenchers want interviews at police stations to be tape-recorded, and every suspect to have the right to see a solicitor.""",
        amend_yes=('Accept the amendment.', 'The Liberals and the wets approve. The police federation does not.',
                   'lib_relation += 3; wet_dissent -= 2; right_dissent += 2',
                   'Tape-recorders will be installed in every interview room, and the duty solicitor will be a phone call away.'),
        amend_no=('Reject it.', 'The right approves. The civil liberties lobby does not.',
                  'lib_relation -= 2; wet_dissent += 2; right_dissent -= 1',
                  'The amendment is defeated. The police will keep their own notes of interviews, as they always have.'),
        lords_title='The Lords Amend the Police and Criminal Evidence Bill',
        lords_text="""The House of Lords votes to protect confidential records held by doctors, clergy and journalists from police search warrants, unless a judge agrees.""",
        lords_yes=('Accept the Lords amendment.', 'The professions are relieved.',
                   'wet_dissent -= 1; lib_relation += 2',
                   "The police will need a circuit judge's order before they search a doctor's files or a newsroom."),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'right_dissent -= 1; wet_dissent += 2; lib_relation -= 1'),
        law="""pace_act = 1; c2_con += 1*(1-dissent); right_dissent -= 2; right_dissent += 2 if bill_pace_watered = 1""",
        law_text="""The Police and Criminal Evidence Act [+ year +] receives Royal Assent. For the first time, the powers of the police and the rights of suspects are written down in one place, with codes of practice for every stage from the stop in the street to the cell door.""",
        achievement='pace'),
    dict(
        key='telecoms', name='Telecommunications Bill', act='Telecommunications Act',
        faction='wet', weight=0.25, champion='dry', committee=3, lords=2, amend=0.35, lords_risk=0.2,
        lib='abstain', ulster='abstain',
        second="""The Telecommunications Bill ends British Telecom's monopoly, creates a regulator, and lets the government sell more than half of the company, in what would be the largest share issue the world has ever seen. The Post Office Engineering Union is campaigning against it, and Labour promises to take British Telecom back into public ownership.""",
        amend_title='In Committee: the Telecommunications Bill',
        amend_text="""Backbenchers from rural seats want a guarantee that a private British Telecom will keep the call boxes and the lines to the remote farms that will never make it a penny.""",
        amend_yes=('Accept the amendment.', 'The shires are content.',
                   'wet_dissent -= 2; dry_dissent += 1',
                   "British Telecom's licence will oblige it to keep a universal service, including the red telephone boxes in the villages."),
        amend_no=('Reject it.', 'The regulator can sort it out later.',
                  'wet_dissent += 2; dry_dissent -= 1; rebellion += 0.2',
                  'The amendment is defeated. The new regulator will have to make the case for the call boxes.'),
        lords_title='The Lords Amend the Telecommunications Bill',
        lords_text="""The House of Lords votes to give the new regulator power to cap British Telecom's prices for ordinary customers.""",
        lords_yes=('Accept the Lords amendment.', 'The shares will be worth a little less.',
                   'wet_dissent -= 1; bill_telecoms_watered = 1',
                   'The regulator will cap prices. The City says the shares will have to be priced more cheaply.'),
        lords_no=('Overturn it in the Commons.', 'The Lords may back down, or may not.',
                  'dry_dissent -= 1; wet_dissent += 1'),
        law="""privatisations += 1; telecoms_sold = 1; budget += 3; budget -= 0.5 if bill_telecoms_watered = 1; economic_liberalism += 3; ab_con += 1*(1-dissent); c1_con += 1*(1-dissent)""",
        law_text="""The Telecommunications Act [+ year +] receives Royal Assent. British Telecom will be sold. The advertising agencies are already competing to sell the shares to people who have never owned one.""",
        achievement='telecoms'),
]

# ---- shared definitions for the generic scenes ----
defs = {}
for b in BILLS:
    defs[b['key']] = {k: b[k] for k in ['name', 'act', 'faction', 'weight', 'champion', 'committee', 'lords',
                                        'amend', 'lords_risk', 'lib', 'ulster']}
fields = ['', '_due', '_time', '_wait', '_watered', '_tough', '_amend', '_lords', '_fast', '_insisted', '_fell']
with open(os.path.join(out_dir, 'bill_defs.scene.dry'), 'w') as f:
    f.write("""title: Bill Definitions
on-arrival: {!
// Generated by gen_bills.py. Each bill: its faction of likely rebels and how
// strongly they object (weight), the faction annoyed by concessions (champion),
// months in committee and in the Lords, the chance of an amendment in
// committee and of a defeat in the Lords, and how the Liberals and the Ulster
// Unionists vote on it.
Q.bill_defs = %s;
Q.bill_keys = %s;
for (var k of Q.bill_keys) {
    for (var f of %s) {
        if (Q['bill_' + k + f] === undefined) {
            Q['bill_' + k + f] = 0;
        }
    }
}
!}

# Shared data for the legislative system. Run from root and from the other bill scenes.
""" % (json.dumps(defs, indent=1), json.dumps([b['key'] for b in BILLS]), json.dumps(fields)))

# ---- per-bill events ----
WHIP = """**The whips' count.** [? if div_proj_rebels >= 1 : About [+ div_proj_rebels +] Conservatives are expected to vote against, and [+ div_proj_abstain +] more to abstain. ?][? if div_proj_rebels = 0 : The party is solid behind the bill. ?][? if div_partner_n = 1 : [+ div_partner_text +] ?] [? if div_proj_majority > 0 : The whips expect a majority of [+ div_proj_majority +]. ?][? if div_proj_majority <= 0 : The whips expect the government to lose by [+ div_proj_deficit +] votes. ?]"""

RESULT = """[? if div_passed = 1 : **Ayes [+ div_ayes +], Noes [+ div_noes +].** The bill is read a second time, with a majority of [+ div_majority +], and goes upstairs to a standing committee. ?][? if div_passed = 0 : **Ayes [+ div_ayes +], Noes [+ div_noes +].** The government is defeated by [+ div_deficit +] votes, and the Opposition benches erupt. The bill is lost, and can't be brought back for a year. ?]

[? if div_rebels >= 1 : [+ div_rebels +] Conservatives voted against the government, and about [+ div_abstain +] more stayed away. ?][? if div_rebels = 0 : Every Conservative in the House voted with the government. ?]"""

out = []
out.append("""title: The Wash-Up
tags: event
view-if: wash_up_pending = 1
new-page: true
on-arrival: wash_up_pending = 0
face-image: img/events/westminster.jpg

= The Wash-Up

With Parliament about to be dissolved for the election, the whips sort out what can be saved. [? if wash_up_passed_n >= 1 : In the last days of the session, the whips agree with the Opposition to rush through the bills that have nearly finished their passage: [+ wash_up_passed +]. ?][? if wash_up_fell_n >= 1 : Bills that have not yet reached the Lords fall, and will have to start again in the next Parliament: [+ wash_up_fell +]. ?]
""")

for b in BILLS:
    k = b['key']
    champion = FACTION_NAME[b['champion']]
    out.append(f"""#################### {b['name']}

@second_{k}
title: Second Reading: the {b['name']}
tags: event
view-if: con_in_government = 1 and in_campaign = 0 and bill_{k} = 1 and bill_{k}_due <= time
new-page: true
on-arrival: div_key = "{k}"; div_mode = "count"
call: bill_vote
face-image: img/events/commons_1970s.jpg

= Second Reading: the {b['name']}

{b['second']}

{WHIP}

- @divide_{k}: Divide the House.
- @concede_{k}: Buy off the rebels with concessions.
- @confidence_{k}: Make it a matter of confidence.
- @deal_{k}: Do a deal with the minor parties.
- @withdraw_{k}: Withdraw the bill.

@divide_{k}
subtitle: Put it to the vote as it stands.
on-arrival: div_key = "{k}"; div_mode = "press"
call: bill_vote

The division bells ring across Westminster, and the members file through the lobbies.

{RESULT}

@concede_{k}
view-if: div_proj_rebels >= 4
subtitle: Most rebels come back. The bill is weakened, and {champion} are annoyed.
on-arrival: div_key = "{k}"; div_mode = "concede"
call: bill_vote

The minister promises the rebels changes in committee, and the whips spend the afternoon in the tea room explaining what they mean.

{RESULT}

@confidence_{k}
view-if: div_proj_majority < 30
subtitle: Most rebels will fall into line. They won't forget it.
on-arrival: div_key = "{k}"; div_mode = "confidence"
call: bill_vote

The Chief Whip tells every Conservative member that a defeat tonight would bring down the government.

{RESULT}

@deal_{k}
view-if: govt_type >= 2
subtitle: -1 resource. The minor parties vote with us this time.
choose-if: resources >= 1
unavailable-subtitle: Requires 1 resource.
on-arrival: div_key = "{k}"; div_mode = "deal"
call: bill_vote

A road here, a factory there, and a promise about the next bill. The minor parties agree to support us on this one.

{RESULT}

@withdraw_{k}
view-if: div_proj_majority < 20
subtitle: Avoids a defeat. The bill can come back in six months.
on-arrival: bill_{k} = 0; bill_{k}_wait = time + 6; {b['champion']}_dissent += 3; thatcher_rating -= 1

The bill is withdrawn before the vote. The papers call it a climbdown, and {champion} call it worse.

@amend_{k}
title: {b['amend_title']}
tags: event
view-if: con_in_government = 1 and in_campaign = 0 and bill_{k} = 2 and bill_{k}_amend = 1
new-page: true
face-image: img/events/commons_1970s.jpg

= {b['amend_title']}

{b['amend_text']}

- @amend_yes_{k}: {b['amend_yes'][0]}
- @amend_no_{k}: {b['amend_no'][0]}

@amend_yes_{k}
subtitle: {b['amend_yes'][1]}
on-arrival: {b['amend_yes'][2]}; bill_{k} = 3; bill_{k}_amend = 2; bill_{k}_due = time + 1

{b['amend_yes'][3]}

@amend_no_{k}
subtitle: {b['amend_no'][1]}
on-arrival: {b['amend_no'][2]}; bill_{k} = 3; bill_{k}_amend = 2; bill_{k}_due = time + 1

{b['amend_no'][3]}

@lords_{k}
title: {b['lords_title']}
tags: event
view-if: con_in_government = 1 and bill_{k} = 4 and bill_{k}_lords = 1
new-page: true
face-image: img/events/westminster.jpg

= {b['lords_title']}

{b['lords_text']}

- @lords_yes_{k}: {b['lords_yes'][0]}
- @lords_no_{k}: {b['lords_no'][0]}

@lords_yes_{k}
subtitle: {b['lords_yes'][1]}
on-arrival: {b['lords_yes'][2]}; bill_{k}_lords = 2; bill_{k}_due = time + 1

{b['lords_yes'][3]} Royal Assent should follow within the month.

@lords_no_{k}
subtitle: {b['lords_no'][1]}
on-arrival: {b['lords_no'][2]}; lords_key = "{k}"
call: bill_insist

The whips bring the clause back to the Commons, and the government's majority reverses the Lords. [? if lords_gave_way = 1 : The peers decide not to press the point a second time, and the bill goes through as the government wanted. ?][? if lords_gave_way = 0 : The peers insist. After a month of messages between the two Houses, the government gives way to save the bill, with nothing to show for the delay. ?]

@assent_{k}
title: Royal Assent: the {b['act']}
tags: event
view-if: bill_{k} = 5
new-page: true
on-arrival: {b['law']}; bill_{k} = 6; assent_key = "{k}"
call: bill_assent
face-image: img/events/westminster.jpg
""" + (f"achievement: {b['achievement']}\n" if b['achievement'] else '') + f"""
= Royal Assent: the {b['act']}

{b['law_text']}
""")

with open(os.path.join(out_dir, 'bills.scene.dry'), 'w') as f:
    f.write('\n'.join(out))
print('wrote', len(BILLS), 'bills')
