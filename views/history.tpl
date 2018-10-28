% rebase('base.tpl', title=title, itson=itson)
<div class="row back">
    <table class="table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Spot</th>
                <th class="no-mobile">Started</th>
                <th class="no-mobile">Ended</th>
                <th>Duration</th>
                <th>Waves</th>
                <th class="no-mobile">Comment</th>
            </tr>
        </thead>
        <tbody>
        % for r in sessions:
            <tr>
                <td>{{r['date']}}</td>
                <td>{{r['spot']}}</td>
                <td class="no-mobile">{{r['started']}}</td>
                <td class="no-mobile">{{r['ended'] or "Its ON!"}}</td>
                <td>{{r['duration'] or "Its ON!"}}</td>
                <td>{{r['size']}}</td>
                <td class="no-mobile">{{r['comment'] or ""}}</td>
            </tr>
        % end
        </tbody>
    </table>
</div>
